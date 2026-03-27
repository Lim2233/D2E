"""
自动化测试主脚本
用于运行所有测试并生成测试报告
"""
import sys
import os
import unittest
import json
from datetime import datetime

# 添加项目根目录和backend目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'backend'))


class TestConfig:
    """
    测试配置
    """
    # 测试报告目录
    REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tests', 'reports')
    
    # 测试文件路径
    TEST_FILES = [
        'backend.tests.test_parser',
        'backend.tests.test_extractor',
        'backend.tests.test_matcher'
    ]
    
    # 是否生成详细报告
    VERBOSE = True


class TestRunner:
    """
    测试运行器
    """
    
    def __init__(self):
        """
        初始化测试运行器
        """
        self.results = {}
        self.start_time = None
        self.end_time = None
    
    def run_all_tests(self):
        """
        运行所有测试
        """
        print("开始运行自动化测试...")
        print("=" * 60)
        
        self.start_time = datetime.now()
        
        # 确保报告目录存在
        os.makedirs(TestConfig.REPORT_DIR, exist_ok=True)
        
        # 运行每个测试文件
        for test_file in TestConfig.TEST_FILES:
            print(f"\n运行测试: {test_file}")
            print("-" * 40)
            
            try:
                # 导入测试模块
                test_module = __import__(test_file, fromlist=[''])
                
                # 创建测试套件
                test_suite = unittest.TestLoader().loadTestsFromModule(test_module)
                
                # 运行测试
                runner = unittest.TextTestRunner(verbosity=2 if TestConfig.VERBOSE else 1)
                result = runner.run(test_suite)
                
                # 记录结果
                self.results[test_file] = {
                    'success': result.wasSuccessful(),
                    'tests_run': result.testsRun,
                    'failures': len(result.failures),
                    'errors': len(result.errors)
                }
                
            except Exception as e:
                print(f"运行测试时出错: {e}")
                self.results[test_file] = {
                    'success': False,
                    'tests_run': 0,
                    'failures': 1,
                    'errors': 0,
                    'error_message': str(e)
                }
        
        self.end_time = datetime.now()
        self.generate_report()
        self.print_summary()
    
    def generate_report(self):
        """
        生成测试报告
        """
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'duration': str(self.end_time - self.start_time),
            'results': self.results,
            'summary': {
                'total_tests': sum(r['tests_run'] for r in self.results.values()),
                'total_failures': sum(r['failures'] for r in self.results.values()),
                'total_errors': sum(r['errors'] for r in self.results.values()),
                'overall_success': all(r['success'] for r in self.results.values())
            }
        }
        
        # 生成报告文件名
        report_filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(TestConfig.REPORT_DIR, report_filename)
        
        # 写入报告文件
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n测试报告已生成: {report_path}")
    
    def print_summary(self):
        """
        打印测试摘要
        """
        print("\n" + "=" * 60)
        print("测试摘要")
        print("=" * 60)
        
        total_tests = sum(r['tests_run'] for r in self.results.values())
        total_failures = sum(r['failures'] for r in self.results.values())
        total_errors = sum(r['errors'] for r in self.results.values())
        overall_success = all(r['success'] for r in self.results.values())
        
        print(f"开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"结束时间: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"持续时间: {self.end_time - self.start_time}")
        print(f"总测试数: {total_tests}")
        print(f"失败数: {total_failures}")
        print(f"错误数: {total_errors}")
        print(f"成功率: {((total_tests - total_failures - total_errors) / total_tests * 100):.2f}%" if total_tests > 0 else "0%")
        print(f"整体结果: {'通过' if overall_success else '失败'}")
        
        print("\n各测试模块结果:")
        for test_file, result in self.results.items():
            status = "通过" if result['success'] else "失败"
            print(f"- {test_file}: {status} (运行: {result['tests_run']}, 失败: {result['failures']}, 错误: {result['errors']})")
        
        print("\n" + "=" * 60)


if __name__ == "__main__":
    runner = TestRunner()
    runner.run_all_tests()
    
    # 根据测试结果设置退出码
    overall_success = all(r['success'] for r in runner.results.values())
    sys.exit(0 if overall_success else 1)
