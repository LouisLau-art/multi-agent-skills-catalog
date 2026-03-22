import os
from pathlib import Path

skills_dir = Path("/home/louis/.codex/skills")
if not skills_dir.exists():
    print("Skills dir not found")
    exit(1)

count = sum(1 for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith("."))
print(f"Total skills: {count}")
