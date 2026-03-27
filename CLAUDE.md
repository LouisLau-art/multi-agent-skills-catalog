# CLAUDE.md

## 项目概述
多Agent技能目录与跨平台同步系统，提供经过质量筛选的生产级Agent技能分发服务，支持Claude/Codex/Gemini等主流AI Agent运行时。

## 技术栈
- Python, CLI开发, GitHub Pages, GitHub Actions, Context7 API, Jinja2

## 常用命令

### 安装技能
```bash
# 安装默认公共配置到Claude
python scripts/install_curated.py claude --profiles public-default

# 安装全部公共技能
python scripts/install_curated.py claude --profiles all-public

# 跨Agent同步
python scripts/install_curated.py all --profiles public-default

# 列出可用配置
python scripts/install_curated.py --list-profiles
```

### 数据更新
```bash
# 拉取skills.sh排名
python scripts/fetch_skills_sh_rankings.py --view all-time --limit 2000 --output-json docs/data/skills_sh_all_time_top2000.json

# 拉取Context7技能排名
python scripts/fetch_context7_skill_rankings.py --min-installs 0 --output-csv data/context7_ranked_skills_all.csv

# 拉取Context7文档排名
python scripts/fetch_context7_library_rankings.py --kind popular --output-csv data/context7_popular_libraries.csv
```

### 本地开发
```bash
# 启动本地预览站点
cd docs
python -m http.server 8000

# 验证技能元数据
python scripts/validate_skills_frontmatter.py
```

## 项目架构
```
技能数据源 (skills.sh + Context7 API)
    ↓
[fetch_*.py] → 原始数据 (data/)
    ↓
[rebuild_*.py] → 分类与聚合
    ↓
[jinja2模板] → 静态站点 (docs/)
    ↓
GitHub Pages → 用户访问
```

## 关键文件
| 路径 | 用途 |
|------|------|
| `skills_manifest.csv` | 精选技能清单 |
| `profiles/*.txt` | 安装配置包 |
| `scripts/install_curated.py` | 跨平台安装器 |
| `docs/index.html` | 静态站点首页 |
| `.github/workflows/` | 自动更新工作流 |

## 部署
- 站点自动部署到GitHub Pages，通过GitHub Actions每日更新排名数据
- 无需手动部署，推送main分支自动触发构建

## 开发约定
- 技能选择遵循去重策略：每个主题仅保留1-2个最优技能
- 优先选择官方或高维护性来源的技能
- 所有脚本兼容Windows/macOS/Linux三平台
- 不存储第三方技能文件，仅提供分发层

## 常见问题
- **安装失败**: 检查网络连接、CONTEXT7_API_KEY是否配置正确
- **技能不生效**: 检查Agent的技能目录配置是否正确
- **站点更新慢**: GitHub Actions每日自动更新，可手动触发workflow