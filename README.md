# Test Plan Generator Skill

测试计划自动生成器 - 基于旧版测试计划和版本变更点，自动生成符合规范的新版测试计划文档。

## 功能特性

- 📄 **智能解析** - 自动解析旧版测试计划结构（支持 Markdown/JSON/DOCX）
- 🔍 **变更分析** - 智能分析版本变更对测试范围的影响
- 📋 **策略生成** - 根据变更类型自动生成测试策略
- ✨ **用例推导** - 自动生成新增/修改的测试用例
- 📊 **多格式输出** - 支持 Markdown/JSON/DOCX 格式输出
- ✅ **质量检查** - 内置质量检查机制，确保文档完整性

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基础用法

```bash
python testplan_generator.py \
  --old-plan tests/sample_old_plan.md \
  --changes "新增用户登录功能;修复支付bug" \
  --output workspace-dev/reports/new_testplan.md
```

### 参数说明

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `--old-plan` | 旧版测试计划文件路径 | 是 | - |
| `--changes` | 版本变更点（用分号分隔） | 是 | - |
| `--output` | 输出文件路径 | 否 | workspace-dev/reports/testplan_YYYYMMDD_HHMMSS.md |
| `--format` | 输出格式（markdown/json/docx） | 否 | markdown |
| `--version` | 新版本号 | 否 | 自动递增 |

## 使用示例

### 示例1：生成Markdown格式测试计划

```bash
python testplan_generator.py \
  --old-plan tests/sample_old_plan.md \
  --changes "新增API接口;优化数据库查询性能" \
  --output reports/testplan_v2.0.md
```

**输出：**
```
============================================================
测试计划自动生成器
============================================================

[1/6] 解析旧测试计划...
  ✓ 版本: 1.0
  ✓ 测试范围: 3 项
  ✓ 测试用例: 5 个

[2/6] 分析变更影响...
  ✓ 新功能: 1 项
  ✓ Bug修复: 0 项
  ✓ 性能优化: 1 项

[3/6] 生成测试策略...
  ✓ 生成 3 项测试策略

[4/6] 生成测试用例...
  ✓ 生成 2 个新测试用例

[5/6] 组装文档...
  ✓ 文档格式: markdown
  ✓ 新版本: 1.1

[6/6] 质量检查...
  ✓ 质量检查通过

保存文件到: reports/testplan_v2.0.md

============================================================
✓ 测试计划生成完成!
============================================================
```

### 示例2：生成JSON格式

```bash
python testplan_generator.py \
  --old-plan tests/sample_old_plan.md \
  --changes "修复登录bug;新增导出功能" \
  --format json \
  --output reports/testplan_v2.0.json
```

### 示例3：指定版本号

```bash
python testplan_generator.py \
  --old-plan tests/sample_old_plan.md \
  --changes "重构前端架构;升级依赖库" \
  --version "2.1.0"
```

## 输入格式

### 旧测试计划格式（Markdown）

```markdown
# 测试计划 - 版本 1.0

## 1. 测试范围
- 用户管理模块
- 订单处理模块

## 2. 测试策略
- 功能测试
- 性能测试

## 3. 测试用例
### TC001: 用户登录
**前置条件:** 用户已注册
**测试步骤:**
1. 输入用户名密码
2. 点击登录
**预期结果:** 登录成功
```

### 变更点格式

使用分号分隔多个变更点：
```
"新增用户注册功能;修复登录超时bug;优化数据库查询性能"
```

## 输出格式

### Markdown 输出

生成的测试计划包含以下章节：
1. 版本变更摘要
2. 测试范围
3. 测试策略
4. 测试用例（回归 + 新增）
5. 测试资源
6. 测试进度

### JSON 输出

```json
{
  "version": "1.1",
  "generated_at": "2026-03-09T21:09:15",
  "changes": {
    "new_features": ["新增用户注册功能"],
    "bug_fixes": ["修复登录超时bug"],
    "optimizations": ["优化数据库查询性能"]
  },
  "test_scope": ["用户管理模块", "订单处理模块"],
  "test_strategy": [...],
  "test_cases": {
    "regression": [...],
    "new": [...]
  }
}
```

## 处理流程

```
输入解析 → 变更影响分析 → 测试策略生成 → 测试用例推导 → 文档组装 → 质量控制
```

1. **输入解析** - 解析旧测试计划结构和变更点
2. **变更影响分析** - 分析变更对测试范围的影响
3. **测试策略生成** - 根据变更类型生成测试策略
4. **测试用例推导** - 自动生成新增/修改的测试用例
5. **文档组装** - 组装完整的测试计划文档
6. **质量控制** - 检查文档完整性和合规性

## 质量检查

自动检查以下项目：
- ✅ 所有变更点都有对应的测试用例
- ✅ 测试用例编号连续且唯一
- ✅ 必需章节完整（测试范围、策略、用例）
- ✅ 测试用例包含必要字段

## 项目结构

```
testplan_skill/
├── README.md                    # 项目说明
├── SKILL.md                     # Skill文档
├── requirements.txt             # 依赖列表
├── testplan_generator.py        # 主程序
├── tests/                       # 测试文件
│   └── sample_old_plan.md      # 示例测试计划
└── workspace-dev/               # 输出目录
    └── reports/                 # 生成的测试计划
```

## 依赖

- Python 3.8+
- python-docx (用于DOCX格式输出)
- markdown (用于Markdown解析)

## 开发

### 运行测试

```bash
# 测试Markdown输出
python testplan_generator.py \
  --old-plan tests/sample_old_plan.md \
  --changes "新增功能;修复bug" \
  --output workspace-dev/reports/test.md

# 测试JSON输出
python testplan_generator.py \
  --old-plan tests/sample_old_plan.md \
  --changes "新增功能;修复bug" \
  --format json \
  --output workspace-dev/reports/test.json
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可

MIT License

## 作者

Kiro AI Assistant

## 版本历史

- **1.0.0** (2026-03-09)
  - 初始版本
  - 支持Markdown和JSON格式输出
  - 实现6阶段处理流程
  - 内置质量检查机制

## 联系方式

GitHub: https://github.com/siyiding/testplan_skill
