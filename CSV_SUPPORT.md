# CSV格式支持说明

## 概述

测试计划生成器现已支持CSV格式的测试用例文件，可以更灵活地组织和管理测试用例。

## 新功能特性

### 1. 自动扫描CSV文件
- 自动识别`testcase*.csv`格式的文件
- 支持多个CSV文件同时解析
- 自动合并所有测试用例

### 2. 支持目录输入
- 可以传入目录路径而非单一文件
- 自动扫描目录下所有CSV文件
- 与Markdown测试计划文件配合使用

### 3. 灵活的文件组织
支持两种组织方式：

**方式1：Markdown + CSV（推荐）**
```
tests/
├── testplan_v1.0.md          # 测试计划主文件（测试范围、策略等）
├── testcase_v1.0.csv         # 基础测试用例
└── testcase_v2.0.csv         # 新增测试用例
```

**方式2：纯CSV**
```
tests/
├── testcase_module1.csv      # 模块1测试用例
├── testcase_module2.csv      # 模块2测试用例
└── testcase_module3.csv      # 模块3测试用例
```

## CSV文件格式

### 必需列

| 列名 | 说明 | 示例 |
|------|------|------|
| ID | 测试用例ID | TC001, TC002 |
| 标题 | 测试用例标题 | 用户登录功能测试 |
| 步骤 | 测试步骤 | 1. 打开登录页面<br>2. 输入用户名密码 |
| 预期结果 | 预期结果 | 登录成功并跳转到首页 |

### 可选列

| 列名 | 说明 | 示例 |
|------|------|------|
| 模块 | 所属模块 | 用户管理、订单管理 |
| 类型 | 测试类型 | 功能测试、性能测试 |
| 前置条件 | 执行前提 | 用户已注册 |
| 优先级 | 优先级 | 高、中、低 |
| 状态 | 执行状态 | 通过、待测试、失败 |

### CSV示例

```csv
ID,模块,类型,标题,前置条件,步骤,预期结果,优先级,状态
TC001,用户管理,功能测试,用户登录,用户已注册,"1. 打开登录页面
2. 输入用户名和密码
3. 点击登录按钮",登录成功并跳转到首页,高,通过
TC002,用户管理,功能测试,用户注册,无,"1. 打开注册页面
2. 填写用户信息
3. 点击注册按钮",注册成功并自动登录,高,通过
TC003,订单管理,功能测试,创建订单,用户已登录,"1. 选择商品
2. 添加到购物车
3. 提交订单",订单创建成功,高,通过
```

**注意事项：**
1. 步骤字段支持换行，需要用双引号包裹
2. 文件必须使用UTF-8编码
3. 文件名必须以`testcase`开头

## 使用方法

### 方法1：Markdown文件 + CSV文件

```bash
# 目录结构
tests/
├── testplan_v1.0.md
├── testcase_v1.0.csv
└── testcase_v2.0.csv

# 运行命令
python testplan_generator.py \
  --old-plan tests/testplan_v1.0.md \
  --changes "新增会员系统;修复支付bug" \
  --output reports/testplan_v2.0.md
```

**输出：**
```
[1/6] 解析旧测试计划...
  → 解析CSV: testcase_v1.0.csv
  → 解析CSV: testcase_v2.0.csv
  ✓ 从CSV文件加载: 8 个用例
  ✓ 版本: 1.0
  ✓ 测试范围: 3 项
  ✓ 测试用例: 8 个
```

### 方法2：仅使用目录

```bash
# 目录结构
tests/
├── testcase_module1.csv
├── testcase_module2.csv
└── testcase_module3.csv

# 运行命令
python testplan_generator.py \
  --old-plan tests/ \
  --changes "新增功能;修复bug" \
  --output reports/testplan_new.md
```

## 实际案例

### 案例1：多模块测试用例管理

**文件组织：**
```
project_tests/
├── testplan_main.md              # 主测试计划
├── testcase_user_module.csv     # 用户模块测试用例
├── testcase_order_module.csv    # 订单模块测试用例
├── testcase_payment_module.csv  # 支付模块测试用例
└── testcase_performance.csv     # 性能测试用例
```

**命令：**
```bash
python testplan_generator.py \
  --old-plan project_tests/testplan_main.md \
  --changes "新增会员系统;优化支付流程;修复订单bug" \
  --output reports/testplan_v2.0.md \
  --version "2.0.0"
```

**结果：**
- 自动加载所有4个CSV文件中的测试用例
- 根据变更点生成新的测试策略
- 生成完整的v2.0测试计划

### 案例2：版本迭代测试用例累积

**文件组织：**
```
tests/
├── testplan_v1.0.md
├── testcase_v1.0.csv    # v1.0的测试用例
├── testcase_v1.1.csv    # v1.1新增的测试用例
└── testcase_v1.2.csv    # v1.2新增的测试用例
```

**命令：**
```bash
python testplan_generator.py \
  --old-plan tests/testplan_v1.0.md \
  --changes "新增数据导出;新增报表功能" \
  --output reports/testplan_v2.0.md
```

**结果：**
- 合并v1.0、v1.1、v1.2的所有测试用例
- 基于累积的测试用例生成新版测试计划

## 优势

### 1. 更好的组织性
- 按模块分离测试用例
- 便于团队协作
- 易于版本控制

### 2. 易于维护
- CSV格式易于编辑
- 支持Excel等工具
- 批量导入导出

### 3. 灵活性
- 支持多文件组合
- 支持增量添加
- 支持历史版本保留

### 4. 兼容性
- 与现有Markdown格式兼容
- 可以混合使用
- 平滑迁移

## 迁移指南

### 从纯Markdown迁移到CSV

**步骤1：提取测试用例**

原Markdown格式：
```markdown
### TC001: 用户登录
**前置条件:** 用户已注册
**测试步骤:**
1. 打开登录页面
2. 输入用户名和密码
**预期结果:** 登录成功
```

转换为CSV：
```csv
ID,标题,前置条件,步骤,预期结果
TC001,用户登录,用户已注册,"1. 打开登录页面
2. 输入用户名和密码",登录成功
```

**步骤2：保留测试计划主文件**

保留Markdown文件中的：
- 测试范围
- 测试策略
- 测试资源
- 测试进度

**步骤3：测试验证**

```bash
python testplan_generator.py \
  --old-plan tests/testplan.md \
  --changes "测试迁移" \
  --output reports/testplan_migrated.md
```

## 常见问题

### Q1: CSV文件必须放在哪里？
A: CSV文件应该与Markdown测试计划文件放在同一目录，或者直接传入包含CSV文件的目录路径。

### Q2: 支持哪些CSV文件名？
A: 文件名必须以`testcase`开头，例如：
- ✅ testcase_v1.0.csv
- ✅ testcase_user.csv
- ✅ testcase.csv
- ❌ test_cases.csv
- ❌ cases.csv

### Q3: CSV文件编码要求？
A: 必须使用UTF-8编码，否则可能出现中文乱码。

### Q4: 步骤字段如何换行？
A: 使用双引号包裹，直接在引号内换行：
```csv
"1. 第一步
2. 第二步
3. 第三步"
```

### Q5: 可以混合使用Markdown和CSV吗？
A: 可以！推荐使用Markdown文件定义测试范围和策略，使用CSV文件管理测试用例。

## 版本历史

- **v1.1.0** (2026-03-09)
  - ✨ 新增CSV格式支持
  - ✨ 支持目录输入
  - ✨ 支持多CSV文件合并
  - ✨ 自动扫描testcase*.csv文件

- **v1.0.0** (2026-03-09)
  - 初始版本
  - 支持Markdown格式
  - 支持JSON输出

## 反馈与建议

如有问题或建议，请访问：https://github.com/siyiding/testplan_skill
