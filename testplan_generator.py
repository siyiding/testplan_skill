#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试计划自动生成器
基于旧版测试计划和版本变更点，自动生成新版测试计划文档
"""

import argparse
import json
import re
import os
import csv
from datetime import datetime
from pathlib import Path


class CSVTestCaseParser:
    """CSV测试用例解析器"""
    
    def __init__(self, csv_path):
        self.csv_path = csv_path
    
    def parse(self):
        """解析CSV文件中的测试用例"""
        cases = []
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    case = {
                        'id': row.get('ID', '').strip(),
                        'title': row.get('标题', '').strip(),
                        'module': row.get('模块', '').strip(),
                        'type': row.get('类型', '').strip(),
                        'precondition': row.get('前置条件', '').strip(),
                        'steps': row.get('步骤', '').strip(),
                        'expected': row.get('预期结果', '').strip(),
                        'priority': row.get('优先级', '').strip(),
                        'status': row.get('状态', '').strip(),
                        'content': f"{row.get('标题', '')} - {row.get('类型', '')}"
                    }
                    if case['id']:  # 只添加有ID的用例
                        cases.append(case)
        except Exception as e:
            print(f"  ⚠ 警告: 解析CSV文件 {self.csv_path} 失败: {e}")
        
        return cases


class TestPlanParser:
    """测试计划解析器（支持Markdown文件或目录）"""
    
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.content = self._read_file() if self.file_path.is_file() else ""
        
    def _read_file(self):
        """读取文件内容"""
        if self.file_path.is_file():
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def parse(self):
        """解析测试计划（支持目录或单文件）"""
        plan = {
            'version': self._extract_version(),
            'test_scope': self._extract_test_scope(),
            'test_strategy': self._extract_test_strategy(),
            'test_cases': self._extract_test_cases(),
            'raw_content': self.content
        }
        
        # 如果输入是目录，扫描CSV文件
        if self.file_path.is_dir():
            csv_cases = self._parse_csv_files()
            plan['test_cases'].extend(csv_cases)
            print(f"  ✓ 从CSV文件加载: {len(csv_cases)} 个用例")
        # 如果输入是文件，检查同目录下的CSV文件
        elif self.file_path.is_file():
            csv_cases = self._parse_csv_files_in_same_dir()
            if csv_cases:
                plan['test_cases'].extend(csv_cases)
                print(f"  ✓ 从CSV文件加载: {len(csv_cases)} 个用例")
        
        return plan
    
    def _parse_csv_files(self):
        """解析目录下所有CSV测试用例文件"""
        cases = []
        csv_files = sorted(self.file_path.glob('testcase*.csv'))
        
        for csv_file in csv_files:
            print(f"  → 解析CSV: {csv_file.name}")
            parser = CSVTestCaseParser(csv_file)
            csv_cases = parser.parse()
            cases.extend(csv_cases)
        
        return cases
    
    def _parse_csv_files_in_same_dir(self):
        """解析与测试计划文件同目录下的CSV文件"""
        cases = []
        parent_dir = self.file_path.parent
        csv_files = sorted(parent_dir.glob('testcase*.csv'))
        
        for csv_file in csv_files:
            print(f"  → 解析CSV: {csv_file.name}")
            parser = CSVTestCaseParser(csv_file)
            csv_cases = parser.parse()
            cases.extend(csv_cases)
        
        return cases
    
    def _extract_version(self):
        """提取版本号"""
        match = re.search(r'版本[：:\s]+([0-9.]+)', self.content)
        if match:
            return match.group(1)
        return "1.0"
    
    def _extract_test_scope(self):
        """提取测试范围"""
        scopes = []
        # 查找测试范围章节
        scope_section = re.search(r'##\s*\d*\.?\s*测试范围(.*?)(?=##|\Z)', self.content, re.DOTALL)
        if scope_section:
            content = scope_section.group(1)
            # 提取列表项
            items = re.findall(r'[-*]\s*(.+)', content)
            scopes = [item.strip() for item in items]
        return scopes
    
    def _extract_test_strategy(self):
        """提取测试策略"""
        strategies = []
        strategy_section = re.search(r'##\s*\d*\.?\s*测试策略(.*?)(?=##|\Z)', self.content, re.DOTALL)
        if strategy_section:
            content = strategy_section.group(1)
            items = re.findall(r'[-*]\s*(.+)', content)
            strategies = [item.strip() for item in items]
        return strategies
    
    def _extract_test_cases(self):
        """提取测试用例"""
        cases = []
        # 查找测试用例章节
        case_section = re.search(r'##\s*\d*\.?\s*测试用例(.*?)(?=##|\Z)', self.content, re.DOTALL)
        if case_section:
            content = case_section.group(1)
            # 提取每个测试用例
            case_blocks = re.findall(r'###\s*(TC\d+)[：:]\s*(.+?)(?=###|\Z)', content, re.DOTALL)
            for case_id, case_content in case_blocks:
                case = {
                    'id': case_id,
                    'title': case_content.split('\n')[0].strip(),
                    'content': case_content.strip()
                }
                cases.append(case)
        return cases


class ChangeAnalyzer:
    """变更影响分析器"""
    
    def __init__(self, changes):
        self.changes = self._parse_changes(changes)
    
    def _parse_changes(self, changes_str):
        """解析变更点"""
        if isinstance(changes_str, list):
            return changes_str
        return [c.strip() for c in changes_str.split(';') if c.strip()]
    
    def analyze_impact(self, old_plan):
        """分析变更影响"""
        impact = {
            'new_features': [],
            'bug_fixes': [],
            'optimizations': [],
            'affected_modules': set()
        }
        
        for change in self.changes:
            change_lower = change.lower()
            
            # 分类变更
            if any(keyword in change_lower for keyword in ['新增', '添加', '增加', 'add', 'new']):
                impact['new_features'].append(change)
            elif any(keyword in change_lower for keyword in ['修复', '修改', 'fix', 'bug']):
                impact['bug_fixes'].append(change)
            elif any(keyword in change_lower for keyword in ['优化', '提升', '改进', 'optimize', 'improve']):
                impact['optimizations'].append(change)
            else:
                impact['new_features'].append(change)  # 默认归类为新功能
            
            # 识别受影响的模块
            for scope in old_plan.get('test_scope', []):
                if any(keyword in change for keyword in scope.split()):
                    impact['affected_modules'].add(scope)
        
        impact['affected_modules'] = list(impact['affected_modules'])
        return impact


class TestStrategyGenerator:
    """测试策略生成器"""
    
    def generate(self, impact):
        """生成测试策略"""
        strategies = []
        
        if impact['new_features']:
            strategies.append({
                'type': '功能测试',
                'focus': '新增功能验证',
                'items': impact['new_features']
            })
        
        if impact['bug_fixes']:
            strategies.append({
                'type': '回归测试',
                'focus': 'Bug修复验证',
                'items': impact['bug_fixes']
            })
        
        if impact['optimizations']:
            strategies.append({
                'type': '性能测试',
                'focus': '性能优化验证',
                'items': impact['optimizations']
            })
        
        # 添加基础测试策略
        strategies.append({
            'type': '冒烟测试',
            'focus': '核心功能快速验证',
            'items': ['验证系统基本功能正常']
        })
        
        return strategies


class TestCaseGenerator:
    """测试用例生成器"""
    
    def __init__(self, old_cases):
        self.old_cases = old_cases
        self.next_case_id = self._get_next_case_id()
    
    def _get_next_case_id(self):
        """获取下一个测试用例ID"""
        if not self.old_cases:
            return 1
        
        max_id = 0
        for case in self.old_cases:
            match = re.search(r'TC(\d+)', case['id'])
            if match:
                case_num = int(match.group(1))
                max_id = max(max_id, case_num)
        
        return max_id + 1
    
    def generate_cases(self, impact):
        """生成测试用例"""
        new_cases = []
        
        # 为新功能生成测试用例
        for feature in impact['new_features']:
            case = self._generate_feature_case(feature)
            new_cases.append(case)
        
        # 为Bug修复生成回归测试用例
        for bug_fix in impact['bug_fixes']:
            case = self._generate_regression_case(bug_fix)
            new_cases.append(case)
        
        # 为性能优化生成性能测试用例
        for optimization in impact['optimizations']:
            case = self._generate_performance_case(optimization)
            new_cases.append(case)
        
        return new_cases
    
    def _generate_feature_case(self, feature):
        """生成功能测试用例"""
        case_id = f"TC{self.next_case_id:03d}"
        self.next_case_id += 1
        
        return {
            'id': case_id,
            'title': feature,
            'type': '功能测试',
            'priority': 'high',
            'precondition': '系统正常运行',
            'steps': [
                f'1. 准备测试环境',
                f'2. 执行{feature}相关操作',
                f'3. 验证功能是否正常'
            ],
            'expected': f'{feature}功能正常工作，符合需求规格'
        }
    
    def _generate_regression_case(self, bug_fix):
        """生成回归测试用例"""
        case_id = f"TC{self.next_case_id:03d}"
        self.next_case_id += 1
        
        return {
            'id': case_id,
            'title': bug_fix,
            'type': '回归测试',
            'priority': 'high',
            'precondition': 'Bug已修复',
            'steps': [
                f'1. 重现原Bug场景',
                f'2. 验证Bug是否已修复',
                f'3. 验证相关功能未受影响'
            ],
            'expected': 'Bug已修复，相关功能正常'
        }
    
    def _generate_performance_case(self, optimization):
        """生成性能测试用例"""
        case_id = f"TC{self.next_case_id:03d}"
        self.next_case_id += 1
        
        return {
            'id': case_id,
            'title': optimization,
            'type': '性能测试',
            'priority': 'medium',
            'precondition': '性能测试环境准备完毕',
            'steps': [
                f'1. 配置性能监控工具',
                f'2. 执行性能测试场景',
                f'3. 收集性能数据'
            ],
            'expected': f'{optimization}达到预期性能指标'
        }


class DocumentAssembler:
    """文档组装器"""
    
    def __init__(self, old_plan, impact, strategies, new_cases, version):
        self.old_plan = old_plan
        self.impact = impact
        self.strategies = strategies
        self.new_cases = new_cases
        self.version = version
    
    def assemble_markdown(self):
        """组装Markdown格式文档"""
        doc = []
        
        # 标题
        doc.append(f"# 测试计划 - 版本 {self.version}\n")
        doc.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 版本变更摘要
        doc.append("\n## 1. 版本变更摘要\n")
        all_changes = (self.impact['new_features'] + 
                      self.impact['bug_fixes'] + 
                      self.impact['optimizations'])
        for change in all_changes:
            doc.append(f"- {change}\n")
        
        # 测试范围
        doc.append("\n## 2. 测试范围\n")
        test_scope = set(self.old_plan.get('test_scope', []))
        test_scope.update(self.impact['affected_modules'])
        for scope in sorted(test_scope):
            doc.append(f"- {scope}\n")
        
        # 测试策略
        doc.append("\n## 3. 测试策略\n")
        for strategy in self.strategies:
            doc.append(f"\n### {strategy['type']}\n")
            doc.append(f"**重点:** {strategy['focus']}\n\n")
            for item in strategy['items']:
                doc.append(f"- {item}\n")
        
        # 测试用例
        doc.append("\n## 4. 测试用例\n")
        
        # 保留旧用例
        doc.append("\n### 4.1 回归测试用例（保留）\n")
        for case in self.old_plan.get('test_cases', []):
            doc.append(f"\n#### {case['id']}: {case['title']}\n")
            doc.append(f"**类型:** 回归测试\n")
        
        # 新增用例
        doc.append("\n### 4.2 新增测试用例\n")
        for case in self.new_cases:
            doc.append(f"\n#### {case['id']}: {case['title']}\n")
            doc.append(f"**类型:** {case['type']}\n")
            doc.append(f"**优先级:** {case['priority']}\n")
            doc.append(f"**前置条件:** {case['precondition']}\n")
            doc.append(f"**测试步骤:**\n")
            for step in case['steps']:
                doc.append(f"  {step}\n")
            doc.append(f"**预期结果:** {case['expected']}\n")
        
        # 测试资源
        doc.append("\n## 5. 测试资源\n")
        doc.append("- 测试人员: 待分配\n")
        doc.append("- 测试环境: 测试环境\n")
        doc.append("- 测试工具: 根据需要配置\n")
        
        # 测试进度
        doc.append("\n## 6. 测试进度\n")
        doc.append("| 阶段 | 开始时间 | 结束时间 | 状态 |\n")
        doc.append("|------|---------|---------|------|\n")
        doc.append("| 测试准备 | TBD | TBD | 待开始 |\n")
        doc.append("| 测试执行 | TBD | TBD | 待开始 |\n")
        doc.append("| 测试报告 | TBD | TBD | 待开始 |\n")
        
        return ''.join(doc)
    
    def assemble_json(self):
        """组装JSON格式文档"""
        doc = {
            'version': self.version,
            'generated_at': datetime.now().isoformat(),
            'changes': {
                'new_features': self.impact['new_features'],
                'bug_fixes': self.impact['bug_fixes'],
                'optimizations': self.impact['optimizations']
            },
            'test_scope': list(set(self.old_plan.get('test_scope', []) + 
                                  self.impact['affected_modules'])),
            'test_strategy': [
                {
                    'type': s['type'],
                    'focus': s['focus'],
                    'items': s['items']
                } for s in self.strategies
            ],
            'test_cases': {
                'regression': [
                    {
                        'id': case['id'],
                        'title': case['title'],
                        'type': 'regression'
                    } for case in self.old_plan.get('test_cases', [])
                ],
                'new': [
                    {
                        'id': case['id'],
                        'title': case['title'],
                        'type': case['type'],
                        'priority': case['priority'],
                        'precondition': case['precondition'],
                        'steps': case['steps'],
                        'expected': case['expected']
                    } for case in self.new_cases
                ]
            }
        }
        return json.dumps(doc, ensure_ascii=False, indent=2)


class QualityChecker:
    """质量检查器"""
    
    def check(self, plan_data, new_cases, impact):
        """执行质量检查"""
        issues = []
        
        # 检查1: 所有变更点都有对应的测试用例
        all_changes = (impact['new_features'] + 
                      impact['bug_fixes'] + 
                      impact['optimizations'])
        
        if len(new_cases) < len(all_changes):
            issues.append(f"警告: 变更点数量({len(all_changes)})多于新增测试用例数量({len(new_cases)})")
        
        # 检查2: 测试用例ID唯一性
        case_ids = [case['id'] for case in new_cases]
        if len(case_ids) != len(set(case_ids)):
            issues.append("错误: 测试用例ID存在重复")
        
        # 检查3: 必需章节完整性
        required_sections = ['test_scope', 'test_strategy']
        for section in required_sections:
            if section not in plan_data or not plan_data[section]:
                issues.append(f"警告: 缺少必需章节 {section}")
        
        # 检查4: 测试用例完整性
        for case in new_cases:
            if not all(key in case for key in ['id', 'title', 'type', 'steps', 'expected']):
                issues.append(f"警告: 测试用例 {case.get('id', 'unknown')} 缺少必要字段")
        
        return issues


class TestPlanGenerator:
    """测试计划生成器主类"""
    
    def __init__(self, old_plan_path, changes, output_path=None, output_format='markdown', version=None):
        self.old_plan_path = old_plan_path
        self.changes = changes
        self.output_path = output_path or self._default_output_path()
        self.output_format = output_format.lower()
        self.version = version
    
    def _default_output_path(self):
        """生成默认输出路径"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = Path('workspace-dev/reports')
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / f'testplan_{timestamp}.md'
    
    def generate(self):
        """生成测试计划"""
        print("=" * 60)
        print("测试计划自动生成器")
        print("=" * 60)
        
        # 1. 解析旧测试计划
        print("\n[1/6] 解析旧测试计划...")
        parser = TestPlanParser(self.old_plan_path)
        old_plan = parser.parse()
        print(f"  ✓ 版本: {old_plan['version']}")
        print(f"  ✓ 测试范围: {len(old_plan['test_scope'])} 项")
        print(f"  ✓ 测试用例: {len(old_plan['test_cases'])} 个")
        
        # 2. 分析变更影响
        print("\n[2/6] 分析变更影响...")
        analyzer = ChangeAnalyzer(self.changes)
        impact = analyzer.analyze_impact(old_plan)
        print(f"  ✓ 新功能: {len(impact['new_features'])} 项")
        print(f"  ✓ Bug修复: {len(impact['bug_fixes'])} 项")
        print(f"  ✓ 性能优化: {len(impact['optimizations'])} 项")
        
        # 3. 生成测试策略
        print("\n[3/6] 生成测试策略...")
        strategy_gen = TestStrategyGenerator()
        strategies = strategy_gen.generate(impact)
        print(f"  ✓ 生成 {len(strategies)} 项测试策略")
        
        # 4. 生成测试用例
        print("\n[4/6] 生成测试用例...")
        case_gen = TestCaseGenerator(old_plan['test_cases'])
        new_cases = case_gen.generate_cases(impact)
        print(f"  ✓ 生成 {len(new_cases)} 个新测试用例")
        
        # 5. 组装文档
        print("\n[5/6] 组装文档...")
        new_version = self.version or self._increment_version(old_plan['version'])
        assembler = DocumentAssembler(old_plan, impact, strategies, new_cases, new_version)
        
        if self.output_format == 'json':
            content = assembler.assemble_json()
        else:  # markdown
            content = assembler.assemble_markdown()
        
        print(f"  ✓ 文档格式: {self.output_format}")
        print(f"  ✓ 新版本: {new_version}")
        
        # 6. 质量检查
        print("\n[6/6] 质量检查...")
        checker = QualityChecker()
        issues = checker.check(old_plan, new_cases, impact)
        
        if issues:
            print("  ⚠ 发现以下问题:")
            for issue in issues:
                print(f"    - {issue}")
        else:
            print("  ✓ 质量检查通过")
        
        # 保存文件
        print(f"\n保存文件到: {self.output_path}")
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("\n" + "=" * 60)
        print("✓ 测试计划生成完成!")
        print("=" * 60)
        
        return {
            'output_path': str(self.output_path),
            'version': new_version,
            'old_cases': len(old_plan['test_cases']),
            'new_cases': len(new_cases),
            'issues': issues
        }
    
    def _increment_version(self, old_version):
        """版本号递增"""
        try:
            parts = old_version.split('.')
            parts[-1] = str(int(parts[-1]) + 1)
            return '.'.join(parts)
        except:
            return "2.0"


def main():
    parser = argparse.ArgumentParser(description='测试计划自动生成器')
    parser.add_argument('--old-plan', required=True, help='旧版测试计划文件路径或目录路径（支持CSV格式）')
    parser.add_argument('--changes', required=True, help='版本变更点（用分号分隔）')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--format', default='markdown', choices=['markdown', 'json', 'docx'], 
                       help='输出格式')
    parser.add_argument('--version', help='新版本号')
    
    args = parser.parse_args()
    
    generator = TestPlanGenerator(
        old_plan_path=args.old_plan,
        changes=args.changes,
        output_path=args.output,
        output_format=args.format,
        version=args.version
    )
    
    result = generator.generate()
    
    print(f"\n生成结果:")
    print(f"  输出文件: {result['output_path']}")
    print(f"  新版本: {result['version']}")
    print(f"  保留用例: {result['old_cases']} 个")
    print(f"  新增用例: {result['new_cases']} 个")


if __name__ == '__main__':
    main()
