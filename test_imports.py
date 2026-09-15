"""
快速测试脚本
验证所有模块是否可以正常导入
"""
import sys


def test_imports():
    """测试所有模块导入"""
    print("测试模块导入...")
    print("-" * 50)
    
    modules = [
        'pygame',
        'pandas',
        'matplotlib',
        'docx',
        'numpy'
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"[OK] {module} 导入成功")
        except ImportError as e:
            print(f"[FAIL] {module} 导入失败：{e}")
            return False
    
    print("-" * 50)
    print("[OK] 所有依赖模块导入成功！\n")
    return True


def test_custom_modules():
    """测试自定义模块"""
    print("测试自定义模块...")
    print("-" * 50)
    
    try:
        from config import SCREEN_WIDTH, SCREEN_HEIGHT
        print(f"[OK] config 模块导入成功 (分辨率：{SCREEN_WIDTH}x{SCREEN_HEIGHT})")
    except Exception as e:
        print(f"[FAIL] config 模块导入失败：{e}")
        return False
    
    try:
        from target import Target
        t = Target(100, 100, 50, (255, 0, 0))
        print(f"[OK] target 模块导入成功 (创建目标：{t.x}, {t.y})")
    except Exception as e:
        print(f"[FAIL] target 模块导入失败：{e}")
        return False
    
    try:
        from target_types import FlickTarget, TrackingTarget
        ft = FlickTarget(200, 200, 30, (0, 255, 0))
        tt = TrackingTarget(300, 300, 40, (0, 0, 255))
        print(f"[OK] target_types 模块导入成功 (闪现靶和追踪靶)")
    except Exception as e:
        print(f"[FAIL] target_types 模块导入失败：{e}")
        return False
    
    try:
        from crosshair import Crosshair
        ch = Crosshair()
        print(f"[OK] crosshair 模块导入成功")
    except Exception as e:
        print(f"[FAIL] crosshair 模块导入失败：{e}")
        return False
    
    try:
        from data_tracker import DataTracker
        dt = DataTracker()
        dt.start_session()
        dt.record_click(100, 100, (150, 150), True)
        print(f"[OK] data_tracker 模块导入成功 (记录测试数据)")
    except Exception as e:
        print(f"[FAIL] data_tracker 模块导入失败：{e}")
        return False
    
    try:
        from data_analyzer import DataAnalyzer
        from data_tracker import DataTracker
        dt = DataTracker()
        dt.start_session()
        for i in range(10):
            dt.record_click(100 + i*10, 100, (150, 150), i % 2 == 0)
        analyzer = DataAnalyzer(dt)
        analyzer.process_data()
        metrics = analyzer.get_metrics()
        print(f"[OK] data_analyzer 模块导入成功 (命中率：{metrics['accuracy']:.1f}%)")
    except Exception as e:
        print(f"[FAIL] data_analyzer 模块导入失败：{e}")
        return False
    
    try:
        from data_visualizer import DataVisualizer
        from data_analyzer import DataAnalyzer
        from data_tracker import DataTracker
        dt = DataTracker()
        dt.start_session()
        for i in range(20):
            dt.record_click(100 + i*50, 100 + i*30, (150, 150), i % 3 == 0)
        analyzer = DataAnalyzer(dt)
        analyzer.process_data()
        visualizer = DataVisualizer(analyzer)
        print(f"[OK] data_visualizer 模块导入成功")
    except Exception as e:
        print(f"[FAIL] data_visualizer 模块导入失败：{e}")
        return False
    
    try:
        from report_generator import ReportGenerator
        print(f"[OK] report_generator 模块导入成功")
    except Exception as e:
        print(f"[FAIL] report_generator 模块导入失败：{e}")
        return False
    
    print("-" * 50)
    print("[OK] 所有自定义模块测试通过！\n")
    return True


def main():
    """主函数"""
    print("=" * 50)
    print("Aim Lab 练枪模拟器 - 模块测试")
    print("=" * 50)
    print()
    
    if not test_imports():
        print("\n[FAIL] 测试失败：依赖模块缺失")
        print("请运行：pip install -r requirements.txt")
        sys.exit(1)
    
    if not test_custom_modules():
        print("\n[FAIL] 测试失败：自定义模块错误")
        sys.exit(1)
    
    print("=" * 50)
    print("[OK] 所有测试通过！")
    print("=" * 50)
    print("\n可以运行游戏了：python main.py")
    print("或运行完整测试：python test_full.py")


if __name__ == "__main__":
    main()
