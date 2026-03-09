# 测试计划Skill v1.1 更新说明

## 更新时间
2026-03-09 21:40 UTC

## 版本
v1.1.0

## 新功能

### ✨ 支持CSV格式测试用例文件

#### 1. CSV文件解析
- 新增`CSVTestCaseParser`类
- 自动解析CSV格式的测试用例
- 支持标准CSV格式（ID, 模块, 类型, 标题, 前置条件, 步骤, 预期结果, 优先级, 状态）

#### 2. 目录输入支持
- `--old-plan`参数现在支持目录路径
- 自动扫描目录下所有`testcase*.csv`文件
- 支持与Markdown文件混合使用

#### 3. 多文件合并
- 自动合并多个CSV文件中的测试用例
- 保持测试用例ID的唯一性
- 按文件名排序处理

## 使用方法

### 方式1：Markdown + CSV（推荐）

```bash
# 目录结构
tests/
├── testplan_v1.0.md          # 测试计划主文件
├── testcase_v1.0.csv         # 测试用例CSV
└── testcase_v2.0.csv         # 更多测试用例

# 运行命令
python testplan_generator.py \
  --old-plan tests/testplan_v1.0.md \
  --changes "新增会员系统;修复支付bug" \
  --output reports/testplan_v2.0.md
```

**输出示例：**
```
[1/6] 解析旧测试计划...
  → 解析CSV: testcase_v1.0.csv
  → 解析CSV: testcase_v2.0.csv
  ✓ 从CSV文件加载: 8 个用例
  ✓ 版本: 1.0
  ✓ 测试范围: 3 项
  ✓ 测试用例: 8 个
```

### 方式2：纯目录输入

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

## CSV文件格式

### 必需列
- **ID**: 测试用例ID（如TC001）
- **标题**: 测试用例标题
- **步骤**: 测试步骤（支持换行）
- **预期结果**: 预期结果

### 可选列
- **模块**: 所属模块
- **类型**: 测试类型（功能测试、性能测试等）
- **前置条件**: 执行前提条件
- **优先级**: 优先级（高、中、低）
- **状态**: 执行状态（通过、待测试等）

### CSV示例

```csv
ID,模块,类型,标题,前置条件,步骤,预期结果,优先级,状态
TC001,用户管理,功能测试,用户登录,用户已注册,"1. 打开登录页面
2. 输入用户名和密码
3. 点击登录按钮",登录成功并跳转到首页,高,通过
TC002,订单管理,功能测试,创建订单,用户已登录,"1. 选择商品
2. 添加到购物车
3. 提交订单",订单创建成功,高,通过
```

## 测试结果

### 测试1：Markdown + CSV
```bash
python testplan_generator.py \
  --old-plan tests/testplan_with_csv.md \
  --changes "新增会员系统;修复支付超时bug" \
  --output workspace-dev/reports/testplan_csv_test.md
```

**结果：**
- ✅ 成功解析2个CSV文件
- ✅ 加载8个测试用例
- ✅ 生成完整测试计划
- ✅ 质量检查通过

### 测试2：目录输入
```bash
python testplan_generator.py \
  --old-plan tests/ \
  --changes "新增数据导出功能;优化数据库索引" \
  --output workspace-dev/reports/testplan_dir_test.md
```

**结果：**
- ✅ 成功扫描目录
- ✅ 自动识别CSV文件
- ✅ 合并所有测试用例
- ✅ 生成测试计划

### 测试3：多CSV文件合并
```bash
python testplan_generator.py \
  --old-plan tests/testplan_with_csv.md \
  --changes "新增积分商城;修复会员等级计算错误" \
  --output workspace-dev/reports/testplan_multi_csv.md
```

**结果：**
- ✅ 解析testcase_v1.0.csv（5个用例）
- ✅ 解析testcase_v2.0.csv（3个用例）
- ✅ 合并共8个测试用例
- ✅ 生成完整测试计划

## 代码变更

### 新增文件
- `CSV_SUPPORT.md` - CSV格式支持详细说明
- `tests/testcase_v1.0.csv` - CSV测试用例示例1
- `tests/testcase_v2.0.csv` - CSV测试用例示例2
- `tests/testplan_with_csv.md` - 配合CSV的测试计划示例

### 修改文件
- `testplan_generator.py` - 添加CSV解析功能
  - 新增`CSVTestCaseParser`类
  - 修改`TestPlanParser`支持目录输入
  - 添加`_parse_csv_files()`方法
  - 添加`_parse_csv_files_in_same_dir()`方法
- `SKILL.md` - 更新使用说明
- `README.md` - 更新功能特性
- `test.sh` - 添加CSV测试用例

### Git提交
```
commit 468bebb
feat: 支持CSV格式测试用例文件

新功能：
- 添加CSVTestCaseParser类，支持解析CSV格式测试用例
- 支持目录输入，自动扫描testcase*.csv文件
- 支持多个CSV文件合并
- 自动识别与Markdown文件同目录的CSV文件
```

## 兼容性

### 向后兼容
- ✅ 完全兼容v1.0的Markdown格式
- ✅ 原有功能不受影响
- ✅ 命令行参数保持一致

### 新功能
- ✅ CSV格式支持
- ✅ 目录输入支持
- ✅ 多文件合并支持

## 优势

### 1. 更灵活的文件组织
- 按模块分离测试用例
- 便于团队协作
- 易于版本控制

### 2. 更易于维护
- CSV格式易于编辑
- 支持Excel等工具
- 批量导入导出

### 3. 更好的扩展性
- 支持多文件组合
- 支持增量添加
- 支持历史版本保留

## 文档

### 新增文档
- `CSV_SUPPORT.md` - CSV格式支持完整说明
  - CSV文件格式规范
  - 使用方法和示例
  - 实际案例
  - 迁移指南
  - 常见问题

### 更新文档
- `SKILL.md` - 添加CSV使用说明
- `README.md` - 更新功能特性列表

## GitHub

**仓库地址：** https://github.com/siyiding/testplan_skill

**最新提交：** 468bebb

**推送状态：** ✅ 已推送到main分支

## 下一步计划

### 短期（1-2周）
- [ ] 支持Excel格式（.xlsx）
- [ ] 添加CSV导出功能
- [ ] 优化CSV解析性能

### 中期（1-2月）
- [ ] 支持更多CSV列定义
- [ ] 添加CSV验证功能
- [ ] 支持CSV模板生成

### 长期（3-6月）
- [ ] Web界面支持CSV上传
- [ ] 可视化CSV编辑器
- [ ] CSV与数据库集成

## 总结

✅ **v1.1.0 更新成功完成**

- 新增CSV格式支持
- 支持目录输入
- 支持多文件合并
- 完全向后兼容
- 所有测试通过
- 文档完善
- 代码已推送到GitHub

---

**开发者：** Kiro AI Assistant  
**更新时间：** 2026-03-09 21:40 UTC  
**版本：** v1.1.0
