#!/bin/bash
# 测试计划生成器 - 快速测试脚本

echo "======================================"
echo "测试计划自动生成器 - 快速测试"
echo "======================================"
echo ""

# 创建输出目录
mkdir -p workspace-dev/reports

echo "测试1: 生成Markdown格式测试计划"
echo "--------------------------------------"
python3 testplan_generator.py \
  --old-plan tests/sample_old_plan.md \
  --changes "新增用户注册功能;修复登录超时bug;优化数据库查询性能" \
  --output workspace-dev/reports/testplan_markdown.md

echo ""
echo "测试2: 生成JSON格式测试计划"
echo "--------------------------------------"
python3 testplan_generator.py \
  --old-plan tests/sample_old_plan.md \
  --changes "新增API接口;修复数据同步bug" \
  --format json \
  --output workspace-dev/reports/testplan_json.json

echo ""
echo "测试3: 指定版本号"
echo "--------------------------------------"
python3 testplan_generator.py \
  --old-plan tests/sample_old_plan.md \
  --changes "重构前端架构;升级依赖库" \
  --version "2.0.0" \
  --output workspace-dev/reports/testplan_v2.0.0.md

echo ""
echo "======================================"
echo "测试完成！"
echo "======================================"
echo ""
echo "生成的文件："
ls -lh workspace-dev/reports/
echo ""
echo "查看Markdown输出："
echo "cat workspace-dev/reports/testplan_markdown.md"
echo ""
echo "查看JSON输出："
echo "cat workspace-dev/reports/testplan_json.json"
