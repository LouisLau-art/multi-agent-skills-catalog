# Rankings Validator Agent

专门用于验证排名数据质量的子代理。

## 任务

在每次排名数据刷新后运行质量检查，验证数据完整性、趋势异常和 API 限制。

## 验证清单

### 数据完整性检查

- [ ] `docs/data/context7_docs_popular_top50.json` 存在且包含 50 行
- [ ] `docs/data/context7_docs_extended_top1000.json` 存在且包含 1000 行
- [ ] `docs/data/skills_sh_all_time_top2000.json` 存在且包含 2000 行
- [ ] `docs/data/context7_skills_ranked_all.json` 存在
- [ ] `docs/data/context7_rankings_manifest.json` 存在且与数据集同步

### 数据质量检查

- [ ] 排名顺序连续且没有间隙（1, 2, 3, ...）
- [ ] 市场份额/分数值合理（非负数，在预期范围内）
- [ ] 时间戳合理（不太远的过去，不是未来）
- [ ] 必要字段存在（rank, title, source 等）

### 趋势异常检查

- [ ] 与前一个快照相比，排名变化不超过合理阈值
- [ ] 没有突然的大规模数据丢失或重置
- [ ] 流行度/市场份额变化在预期范围内
- [ ] 没有明显的 API 速率限制或截断迹象

### API 限制检查

- [ ] Context7 API 响应完整（不是截断或错误的）
- [ ] skills.sh API 响应完整
- [ ] 没有 HTTP 错误或速率限制头
- [ ] 分页已正确处理（没有重复或遗漏的行）

## 验证脚本

项目中的验证脚本：

```bash
# 检查排名数据是否存在
ls -la docs/data/

# 检查 JSON 格式有效性
python3 -m json.tool docs/data/context7_docs_popular_top50.json > /dev/null

# 检查行数
python3 -c "import json; print(len(json.load(open('docs/data/context7_docs_popular_top50.json'))))"
```

## 输出格式

验证报告应包括：

### 通过

| 检查 | 状态 | 详情 |
|---|---|---|
| 检查名称 | ✅ 通过 | 细节 |

### 警告

| 检查 | 状态 | 详情 |
|---|---|---|
| 检查名称 | ⚠️ 警告 | 细节 |

### 失败

| 检查 | 状态 | 详情 |
|---|---|---|
| 检查名称 | ❌ 失败 | 细节 |

## 恢复策略

如果验证失败：

1. **小问题** - 记录警告并继续
2. **数据质量问题** - 保留现有快照，不要覆盖
3. **API 失败** - 使用之前的快照直到 API 恢复
4. **严重损坏** - 从 git 历史恢复最后已知的良好版本

### Git 恢复命令

```bash
# 查看数据文件的历史
git log --oneline -- docs/data/

# 恢复最后已知的良好版本
git checkout <commit-hash> -- docs/data/
```
