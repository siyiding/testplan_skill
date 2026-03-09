# Test Plan Generator Skill

## 概述

测试计划自动生成 Skill，基于旧版测试计划和版本变更点，自动生成符合规范的新版测试计划文档。

**✨ 新功能：支持CSV格式测试用例文件！**

## 功能特性

- 📄 解析旧测试计划结构（支持 Markdown/JSON/DOCX）
- 📊 **支持CSV格式测试用例文件** - 自动扫描并解析testcase*.csv文件
- 📁 **支持目录输入** - 可传入目录路径，自动解析所有CSV文件
- 🔍 分析版本变更影响范围
- 📋 生成测试策略和测试用例
- 📊 支持多格式输出（Markdown/JSON/DOCX）
- ✅ 内置质量检查机制

## 使用方法

### 基础用法（Markdown文件）

```bash
python testplan_generator.py \
  --old-plan path/to/old_testplan.md \
  --changes "新增用户登录功能;修复支付bug" \
  --output output/new_testplan.md
```

### 新功能：使用CSV测试用例文件

#### 方式1：Markdown + CSV（推荐）

将测试计划主文件（Markdown）和CSV测试用例文件放在同一目录：

```
tests/
├── testplan_v1.0.md          # 测试计划主文件
├── testcase_v1.0.csv         # 测试用例CSV文件
└── testcase_v2.0.csv         # 更多测试用例
```

运行命令：
```bash
python testplan_generator.py \
  --old-plan tests/testplan_v1.0.md \
  --changes "新增会员系统;修复支付bug" \
  --output reports/testplan_v2.0.md
```

程序会自动：
1. 解析testplan_v1.0.md中的测试范围、策略等信息
2. 扫描同目录下所有testcase*.csv文件
3. 合并所有测试用例
4. 生成新版测试计划

#### 方式2：仅使用目录

如果只有CSV文件，可以直接传入目录：

```bash
python testplan_generator.py \
  --old-plan tests/ \
  --changes "新增功能;修复bug" \
  --output reports/testplan_new.md
```

### CSV文件格式

CSV文件必须包含以下列（表头）：

| 列名 | 说明 | 必需 |
|------|------|------|
| ID | 测试用例ID（如TC001） | 是 |
| 模块 | 所属模块 | 否 |
| 类型 | 测试类型（功能测试/性能测试等） | 否 |
| 标题 | 测试用例标题 | 是 |
| 前置条件 | 执行前提条件 | 否 |
| 步骤 | 测试步骤（支持换行） | 是 |
| 预期结果 | 预期结果 | 是 |
| 优先级 | 优先级（高/中/低） | 否 |
| 状态 | 执行状态（通过/待测试等） | 否 |

**CSV示例：**

```csv
ID,模块,类型,标题,前置条件,步骤,预期结果,优先级,状态
TC001,用户管理,功能测试,用户登录,用户已注册,"1. 打开登录页面
2. 输入用户名和密码
3. 点击登录按钮",登录成功并跳转到首页,高,通过
TC002,订单管理,功能测试,创建订单,用户已登录,"1. 选择商品
2. 添加到购物车
3. 提交订单",订单创建成功,高,通过
```

**注意：**
- CSV文件名必须以`testcase`开头（如testcase_v1.0.csv）
- 支持多个CSV文件，程序会自动合并
- 步骤字段支持换行（用引号包裹）

### 参数说明

- `--old-plan`: 旧版测试计划文件路径或目录路径（必需）
  - 支持单个Markdown文件
  - 支持目录路径（自动扫描CSV文件）
- `--changes`: 版本变更点描述（必需，用分号分隔多个变更）
- `--output`: 输出文件路径（可选，默认：workspace-dev/reports/testplan_YYYYMMDD_HHMMSS.md）
- `--format`: 输出格式（可选，支持：markdown/json/docx，默认：markdown）
- `--version`: 新版本号（可选，默认：自动递增）

### 示例

#### 示例1：基础生成
```bash
python testplan_generator.py \
  --old-plan tests/sample_old_plan.md \
  --changes "新增API接口;优化数据库查询性能" \
  --output reports/testplan_v2.0.md
```

#### 示例2：生成JSON格式
```bash
python testplan_generator.py \
  --old-plan tests/sample_old_plan.md \
  --changes "修复登录bug;新增导出功能" \
  --format json \
  --output reports/testplan_v2.0.json
```

#### 示例3：生成DOCX格式
```bash
python testplan_generator.py \
  --old-plan tests/sample_old_plan.md \
  --changes "重构前端架构;升级依赖库" \
  --format docx \
  --version "2.1.0"
```

## 输入格式

### 旧测试计划格式（Markdown示例）

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
- 前置条件：用户已注册
- 测试步骤：输入用户名密码，点击登录
- 预期结果：登录成功
```

### 变更点格式

使用分号分隔多个变更点：
```
"新增用户注册功能;修复登录超时bug;优化数据库查询性能"
```

## 输出格式

### Markdown 输出示例

```markdown
# 测试计划 - 版本 2.0

## 1. 版本变更摘要
- 新增用户注册功能
- 修复登录超时bug
- 优化数据库查询性能

## 2. 测试范围
- 用户管理模块（新增注册功能）
- 订单处理模块
- 性能优化验证

## 3. 测试策略
- 功能测试（重点：新增注册功能）
- 回归测试（重点：登录bug修复）
- 性能测试（重点：数据库查询优化）

## 4. 测试用例
### TC001: 用户登录（回归）
### TC002: 用户注册（新增）
### TC003: 数据库查询性能（性能）
```

### JSON 输出示例

```json
{
  "version": "2.0",
  "changes": ["新增用户注册功能", "修复登录超时bug"],
  "test_scope": ["用户管理模块", "订单处理模块"],
  "test_strategy": {
    "functional": ["新增注册功能"],
    "regression": ["登录bug修复"],
    "performance": ["数据库查询优化"]
  },
  "test_cases": [
    {
      "id": "TC001",
      "title": "用户登录",
      "type": "regression",
      "priority": "high"
    }
  ]
}
```

## 处理流程

1. **输入解析** - 解析旧测试计划和变更点
2. **变更影响分析** - 分析变更对测试范围的影响
3. **测试策略生成** - 根据变更类型生成测试策略
4. **测试用例推导** - 生成新增/修改的测试用例
5. **文档组装** - 组装完整的测试计划文档
6. **质量控制** - 检查文档完整性和合规性

## 质量检查

自动检查以下项目：
- ✅ 所有变更点都有对应的测试用例
- ✅ 测试用例编号连续且唯一
- ✅ 必需章节完整（测试范围、策略、用例）
- ✅ 测试用例包含必要字段（前置条件、步骤、预期结果）

## 依赖

- Python 3.8+
- python-docx (用于DOCX格式输出)
- markdown (用于Markdown解析)

## 安装

```bash
pip install python-docx markdown
```

## 开发者

Kiro AI Assistant

## 版本

1.0.0 - 2026-03-09
