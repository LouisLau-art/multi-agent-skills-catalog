---
name: catalog-maintenance
description: 维护技能目录 - 刷新排名、验证清单、审核去重
user-invocable: true
---

# Catalog Maintenance Skill

用于维护多代理技能目录的工作流。

## 可用命令

### 刷新所有排名数据

```
/catalog-maintenance refresh
```

拉取最新的 Context7 技能排名、库文档排名和 skills.sh 排行榜数据。

### 验证技能清单

```
/catalog-maintenance validate
```

验证 `skills_manifest.csv` 格式完整性，运行 frontmatter 验证器。

### 审核去重

```
/catalog-maintenance audit
```

根据去重策略审核技能清单，识别重叠和重复项。

### 构建配置文件

```
/catalog-maintenance build-profile <profile-name>
```

构建并测试指定的配置文件安装。

---

## 工作流

### 完整更新流程

1. 刷新排名数据
2. 验证清单格式
3. 审核去重
4. 提交更改

### 配置文件更新流程

1. 编辑 `profiles/*.txt`
2. 验证配置文件组合
3. 测试安装
4. 更新文档

---

## 快速开始

运行完整维护：
```bash
python3 scripts/fetch_context7_skill_rankings.py --min-installs 0 --output-csv data/context7_ranked_skills_all.csv --output-json data/context7_ranked_skills_all.meta.json
python3 scripts/fetch_context7_library_rankings.py --kind popular --output-csv data/context7_popular_libraries.csv --output-json data/context7_popular_libraries.meta.json
python3 scripts/validate_skills_frontmatter.py
```
