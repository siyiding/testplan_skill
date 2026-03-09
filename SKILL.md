# Test Plan Generator Skill

## 概述

测试计划自动生成 Skill，基于旧版测试计划和版本变更点，自动生成符合规范的新版测试计划文档。

## 功能特性

- 📄 解析旧测试计划结构（支持 Markdown/JSON/DOCX）
- 🔍 分析版本变更影响范围
- 📋 生成测试策略和测试用例
- 📊 支持多格式输出（Markdown/JSON/DOCX）
- ✅ 内置质量检查机制

## 使用方法

### 基础用法

```bash
python testplan_generator.py \
  --old-plan path/to/old_testplan.md \
  --changes "新增用户登录功能;修复支付bug" \
  --output output/new_testplan.md
```

### 参数说明

- `--old-plan`: 旧版测试计划文件路径（必需）
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
