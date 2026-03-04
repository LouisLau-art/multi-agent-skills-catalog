#!/usr/bin/env python3
"""Build an extended docs ranking:

- Keep official Top 50 from /api/rankings as authoritative rows.
- Add estimated rows (51+) from /api/libraries/all using a transparent score.

This script is designed for a static dashboard where users want to see
the official leaderboard and a larger "beyond top 50" view.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from context7_auth import build_context7_request


DEFAULT_BASE_URL = "https://context7.com"
DEFAULT_MAX_WORKERS = 12
DEFAULT_RETRIES = 6
DEFAULT_TOP_K = 1000
DEFAULT_OUTPUT_JSON = "docs/data/context7_docs_extended_top1000.json"
DEFAULT_OUTPUT_CSV = "docs/data/context7_docs_extended_top1000.csv"
MAX_RETRY_AFTER_SECONDS = 120.0


def build_request(url: str):
    return build_context7_request(url)


def fetch_json(url: str, timeout: int = 30, retries: int = DEFAULT_RETRIES) -> Any:
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = build_request(url)
            with urlopen(req, timeout=timeout) as resp:  # nosec B310 (trusted host input)
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as exc:
            last_err = exc
            if attempt < retries:
                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                if retry_after and retry_after.strip().isdigit():
                    retry_after_s = float(retry_after.strip())
                    # Fail fast on long server cooldown windows (hours), otherwise jobs appear "hung".
                    if retry_after_s > MAX_RETRY_AFTER_SECONDS:
                        raise RuntimeError(
                            f"HTTP {exc.code} for {url}: Retry-After={int(retry_after_s)}s "
                            f"exceeds cap {int(MAX_RETRY_AFTER_SECONDS)}s"
                        ) from exc
                    sleep_s = retry_after_s
                elif exc.code == 429:
                    sleep_s = min(60.0, 1.5 * (2 ** (attempt - 1)))
                else:
                    sleep_s = 0.4 * attempt
                sleep_s += random.uniform(0.0, 0.25)
                time.sleep(sleep_s)
            continue
        except (URLError, json.JSONDecodeError) as exc:
            last_err = exc
            if attempt < retries:
                time.sleep(0.4 * attempt)
            continue
    if isinstance(last_err, HTTPError):
        raise RuntimeError(f"HTTP {last_err.code} for {url}") from last_err
    if isinstance(last_err, URLError):
        raise RuntimeError(f"Network error for {url}: {last_err}") from last_err
    if isinstance(last_err, json.JSONDecodeError):
        raise RuntimeError(f"Invalid JSON from {url}") from last_err
    raise RuntimeError(f"Failed to fetch {url}")


def parse_dt(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        try:
            dt = datetime.fromisoformat(raw + "T00:00:00+00:00")
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def human_age(dt: datetime | None, now: datetime) -> str:
    if dt is None:
        return ""
    sec = int((now - dt).total_seconds())
    if sec < 0:
        return "0m"
    if sec < 3600:
        return f"{max(1, sec // 60)}m"
    if sec < 86400:
        return f"{sec // 3600}h"
    if sec < 86400 * 30:
        return f"{sec // 86400}d"
    if sec < 86400 * 365:
        return f"{sec // (86400 * 30)}mo"
    return f"{sec // (86400 * 365)}y"


def to_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def to_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return None


def flatten_library_from_settings_version(
    settings: dict[str, Any], version: dict[str, Any], now: datetime
) -> dict[str, Any]:
    source = settings.get("project") or ""
    title = settings.get("title") or source

    last_update_raw = (
        version.get("lastUpdateDate")
        or version.get("lastRunDate")
        or version.get("parseDate")
        or version.get("lastUpdate")
    )
    dt = parse_dt(last_update_raw)

    return {
        "title": title,
        "source": source,
        "type": settings.get("type") or "",
        "tokens": version.get("totalTokens"),
        "snippets": version.get("totalSnippets"),
        "updateUtc": dt.isoformat().replace("+00:00", "Z") if dt else "",
        "updateAgo": human_age(dt, now),
        "trustScore": settings.get("trustScore"),
        "verified": settings.get("verified"),
        "popularityRank": settings.get("popularityRank"),
        "benchmarkScore": version.get("benchmarkScore"),
        "docsRepoUrl": settings.get("docsRepoUrl") or "",
        "docsSiteUrl": settings.get("docsSiteUrl") or settings.get("docsSiteInputUrl") or "",
    }


def fetch_official_top50(base_url: str, retries: int) -> tuple[list[dict[str, Any]], int]:
    ranking_url = f"{base_url.rstrip('/')}/api/rankings"
    payload = fetch_json(ranking_url, retries=retries)
    libraries = payload.get("data", {}).get("libraries", [])
    if not isinstance(libraries, list):
        raise RuntimeError("Unexpected /api/rankings response shape")

    api_calls = 1
    rows: list[dict[str, Any]] = []
    for item in libraries:
        if not isinstance(item, dict):
            continue
        library_id = item.get("libraryId")
        if not isinstance(library_id, str) or not library_id:
            continue

        rows.append(
            {
                "libraryId": library_id,
                "source": library_id,
                "officialRank": item.get("rank"),
                "officialMarketShare": item.get("marketShare"),
            }
        )

    rows.sort(key=lambda x: to_int(x.get("officialRank")) if to_int(x.get("officialRank")) is not None else 10**9)
    return rows, api_calls


def fetch_all_page(
    base_url: str, page: int, retries: int
) -> tuple[int, list[dict[str, Any]], str | None]:
    url = f"{base_url.rstrip('/')}/api/libraries/all?page={page}"
    try:
        payload = fetch_json(url, retries=retries)
        libs = payload.get("libraries", []) if isinstance(payload, dict) else []
        if not isinstance(libs, list):
            return page, [], f"Invalid page payload shape at page={page}"
        out = [lib for lib in libs if isinstance(lib, dict)]
        return page, out, None
    except Exception as exc:
        return page, [], str(exc)


def choose_better(existing: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    # Prefer rows with higher snippets; tie-break with newer update timestamp.
    ex_sn = to_int(existing.get("snippets")) or 0
    ca_sn = to_int(candidate.get("snippets")) or 0
    if ca_sn > ex_sn:
        return candidate
    if ca_sn < ex_sn:
        return existing

    ex_up = existing.get("updateUtc") or ""
    ca_up = candidate.get("updateUtc") or ""
    if ca_up > ex_up:
        return candidate
    return existing


def norm_log(value: float | None, min_log: float, max_log: float) -> float:
    if value is None:
        return 0.0
    lv = math.log1p(max(0.0, value))
    if max_log <= min_log:
        return 0.0
    return (lv - min_log) / (max_log - min_log)


def score_rows(rows: list[dict[str, Any]], now: datetime) -> None:
    pop_vals: list[float] = []
    snippet_vals: list[float] = []
    token_vals: list[float] = []

    for row in rows:
        pr = to_float(row.get("popularityRank"))
        sn = to_float(row.get("snippets"))
        tk = to_float(row.get("tokens"))
        if pr is not None and pr >= 0:
            pop_vals.append(pr)
        if sn is not None and sn >= 0:
            snippet_vals.append(sn)
        if tk is not None and tk >= 0:
            token_vals.append(tk)

    min_log_pop = math.log1p(min(pop_vals)) if pop_vals else 0.0
    max_log_pop = math.log1p(max(pop_vals)) if pop_vals else 1.0
    min_log_sn = math.log1p(min(snippet_vals)) if snippet_vals else 0.0
    max_log_sn = math.log1p(max(snippet_vals)) if snippet_vals else 1.0
    min_log_tk = math.log1p(min(token_vals)) if token_vals else 0.0
    max_log_tk = math.log1p(max(token_vals)) if token_vals else 1.0

    for row in rows:
        pr = to_float(row.get("popularityRank"))
        sn = to_float(row.get("snippets"))
        tk = to_float(row.get("tokens"))
        trust = to_float(row.get("trustScore")) or 0.0
        verified = 1.0 if row.get("verified") is True else 0.0

        pop_norm = norm_log(pr, min_log_pop, max_log_pop)
        # Lower popularityRank is better.
        pop_component = 1.0 - pop_norm if pr is not None else 0.0
        snippet_component = norm_log(sn, min_log_sn, max_log_sn)
        token_component = norm_log(tk, min_log_tk, max_log_tk)
        trust_component = max(0.0, min(1.0, trust / 10.0))

        dt = parse_dt(row.get("updateUtc"))
        age_days = (now - dt).total_seconds() / 86400.0 if dt else 3650.0
        if age_days < 0:
            age_days = 0.0
        recency_component = 1.0 / (1.0 + age_days / 30.0)

        score = (
            0.45 * pop_component
            + 0.20 * snippet_component
            + 0.15 * token_component
            + 0.10 * trust_component
            + 0.05 * verified
            + 0.05 * recency_component
        )

        row["estimatedScore"] = round(score, 6)
        row["score_popularity"] = round(pop_component, 6)
        row["score_snippets"] = round(snippet_component, 6)
        row["score_tokens"] = round(token_component, 6)
        row["score_trust"] = round(trust_component, 6)
        row["score_verified"] = round(verified, 6)
        row["score_recency"] = round(recency_component, 6)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build Context7 extended docs ranking (official top50 + estimated rows)."
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--max-workers", type=int, default=DEFAULT_MAX_WORKERS)
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    parser.add_argument(
        "--max-pages",
        type=int,
        default=0,
        help="Optional cap for /api/libraries/all pages (0 means all pages)",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help="Rows to keep in final output (including official top 50)",
    )
    parser.add_argument("--output-json", default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-csv", default=DEFAULT_OUTPUT_CSV)
    args = parser.parse_args()

    start_ts = time.time()
    now = datetime.now(timezone.utc)
    base_url = args.base_url.rstrip("/")
    retries = max(1, int(args.retries))
    max_workers = max(1, int(args.max_workers))
    top_k = max(50, int(args.top_k))

    official_rows, official_calls = fetch_official_top50(base_url, retries)
    official_sources = {str(r.get("source")) for r in official_rows if r.get("source")}

    page1_payload = fetch_json(f"{base_url}/api/libraries/all?page=1", retries=retries)
    if not isinstance(page1_payload, dict):
        raise RuntimeError("Invalid /api/libraries/all?page=1 payload")
    total_pages = to_int(page1_payload.get("totalPages")) or 1
    page1_libs = page1_payload.get("libraries", [])
    if not isinstance(page1_libs, list):
        raise RuntimeError("Invalid page 1 libraries list")

    page_cap = total_pages
    if int(args.max_pages) > 0:
        page_cap = min(total_pages, int(args.max_pages))

    all_page_map: dict[int, list[dict[str, Any]]] = {1: [x for x in page1_libs if isinstance(x, dict)]}
    page_errors: list[str] = []
    api_calls = official_calls + 1

    pages = list(range(2, page_cap + 1))
    if pages:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            fut_map = {
                executor.submit(fetch_all_page, base_url, page, retries): page
                for page in pages
            }
            for fut in as_completed(fut_map):
                page = fut_map[fut]
                p, libs, err = fut.result()
                api_calls += 1
                if err:
                    page_errors.append(f"page={page}: {err}")
                    continue
                all_page_map[p] = libs

    all_rows: list[dict[str, Any]] = []
    for page in sorted(all_page_map.keys()):
        for lib in all_page_map[page]:
            if not isinstance(lib, dict):
                continue
            settings = lib.get("settings", {})
            version = lib.get("version", {})
            if not isinstance(settings, dict):
                settings = {}
            if not isinstance(version, dict):
                version = {}
            row = flatten_library_from_settings_version(settings, version, now)
            all_rows.append(row)

    by_source: dict[str, dict[str, Any]] = {}
    for row in all_rows:
        source = str(row.get("source") or "").strip()
        if not source:
            continue
        if source not in by_source:
            by_source[source] = row
        else:
            by_source[source] = choose_better(by_source[source], row)

    unique_rows = list(by_source.values())
    score_rows(unique_rows, now)
    by_source_scored = {str(r.get("source")): r for r in unique_rows if r.get("source")}

    final_rows: list[dict[str, Any]] = []
    for row in official_rows:
        source = str(row.get("source") or "")
        scored = by_source_scored.get(source)
        out = dict(scored) if scored else {"title": source, "source": source}
        out["libraryId"] = row.get("libraryId")
        out["officialRank"] = row.get("officialRank")
        out["officialMarketShare"] = row.get("officialMarketShare")
        out["rankType"] = "official"
        out["rank"] = to_int(row.get("officialRank"))
        final_rows.append(out)

    estimated_candidates = [
        r
        for r in unique_rows
        if str(r.get("source") or "") not in official_sources
    ]
    estimated_candidates.sort(
        key=lambda r: (
            -(to_float(r.get("estimatedScore")) or 0.0),
            to_int(r.get("popularityRank")) if to_int(r.get("popularityRank")) is not None else 10**9,
            str(r.get("source") or ""),
        )
    )

    next_rank = len(final_rows) + 1
    for row in estimated_candidates:
        if len(final_rows) >= top_k:
            break
        out = dict(row)
        out["rankType"] = "estimated"
        out["officialRank"] = None
        out["officialMarketShare"] = None
        out["rank"] = next_rank
        next_rank += 1
        final_rows.append(out)

    headers = [
        "rank",
        "rankType",
        "officialRank",
        "officialMarketShare",
        "estimatedScore",
        "title",
        "source",
        "libraryId",
        "popularityRank",
        "snippets",
        "tokens",
        "updateUtc",
        "updateAgo",
        "trustScore",
        "verified",
        "benchmarkScore",
        "type",
        "docsRepoUrl",
        "docsSiteUrl",
        "score_popularity",
        "score_snippets",
        "score_tokens",
        "score_trust",
        "score_verified",
        "score_recency",
    ]

    out_json = Path(args.output_json)
    out_csv = Path(args.output_csv)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(final_rows)

    output = {
        "generatedAtUtc": now.isoformat(),
        "baseUrl": base_url,
        "rows": len(final_rows),
        "officialRows": len(official_rows),
        "estimatedRows": max(0, len(final_rows) - len(official_rows)),
        "topK": top_k,
        "totalPages": total_pages,
        "pagesFetched": len(all_page_map),
        "apiCalls": api_calls,
        "pageErrors": page_errors,
        "scoreModel": {
            "kind": "weighted-normalized",
            "weights": {
                "popularityRankInverse": 0.45,
                "snippetsLogNorm": 0.20,
                "tokensLogNorm": 0.15,
                "trustScoreNorm": 0.10,
                "verified": 0.05,
                "recency": 0.05,
            },
            "notes": [
                "Rows 1-50 remain official rankings from /api/rankings.",
                "Rows >50 are estimated and should be treated as directional.",
            ],
        },
        "items": final_rows,
        "durationSec": round(time.time() - start_ts, 2),
    }
    out_json.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        f"Done. rows={len(final_rows)} official={len(official_rows)} estimated={len(final_rows)-len(official_rows)} "
        f"pages={len(all_page_map)}/{total_pages} api_calls={api_calls} duration={output['durationSec']}s"
    )
    print(f"JSON: {out_json}")
    print(f"CSV:  {out_csv}")
    if page_errors:
        print(f"Warnings: {len(page_errors)} page fetch failures")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
