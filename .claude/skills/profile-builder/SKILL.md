---
name: profile-builder
description: 构建和测试技能配置文件 - 创建、验证、比较配置文件
user-invocable: true
---

# Profile Builder Skill

用于创建和管理技能配置文件的工具。

## 可用命令

### 列出所有配置文件

```
/profile-builder list
```

显示所有可用的公共配置文件及其包含的技能数量。

### 创建新配置文件

```
/profile-builder create <name>
```

交互式创建新的配置文件，从现有技能中选择。

### 验证配置文件

```
/profile-builder validate <name>
```

验证配置文件中的技能是否存在于清单中，检查重复项。

### 比较配置文件

```
/profile-builder compare <profile1> <profile2>
```

显示两个配置文件之间的差异：共同技能、仅在前者、仅在后者。

### 测试配置文件安装

```
/profile-builder test-install <name>
```

干运行安装指定的配置文件，验证安装流程。

### 组合配置文件

```
/profile-builder combine <profile1>+<profile2>+...
```

显示多个配置文件组合后的完整技能列表。

---

## 配置文件规范

配置文件存储在 `profiles/` 目录下，格式为纯文本：

- 每行一个技能 slug
- `#` 开头的行是注释
- 空行被忽略

### 示例

```
# 我的自定义配置文件
git-commit
python-performance-optimization
react-components
```

---

## 内置配置文件

| 配置文件 | 描述 |
|---------|------|
| `core-meta` | 发现、审核、验证、规划、会话连续性 |
| `development-core` | 软件开发入门包 |
| `context7-integration` | Context7 MCP 加可复用文档查找工作流 |
| `writing-blog` | 公共写作/博客入门 |
| `resume-job-search` | 简历和求职入门 |
| `docs-office` | PDF/DOCX/PPTX/办公工作流 |
| `cloud-platform` | Vercel/Supabase/Hugging Face/平台工作流 |
| `design-ui` | 设计和前端重负载工作 |
| `database-data` | 数据库、RAG 和数据工作流 |

### 别名

- `public-default` = `core-meta` + `development-core`
- `all-public` = 所有公共配置文件的并集
