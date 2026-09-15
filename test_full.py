"""
完整功能测试脚本
测试游戏的所有核心功能（无需启动图形界面）
"""
import sys
import time


def test_target_system():
    """测试目标系统"""
    print("\n[测试 1] 目标系统")
    print("-" * 50)
    
    from target import Target
    from target_types import FlickTarget, TrackingTarget
    
    # 测试基类
    t = Target(100, 100, 50, (255, 0, 0))
    assert t.check_click(100, 100) == True, "中心点击应该命中"
    assert t.check_click(200, 200) == False, "远距离点击应该未命中"
    assert t.get_score() == 100, "基础分数应为 100"
    print("✓ Target 基类测试通过")
    
    # 测试闪现靶
    ft = FlickTarget(200, 200, 30, (0, 255, 0))
    assert ft.lifetime == 0.5, "闪现靶生命周期应为 0.5 秒"
    assert ft.get_score() == 150, "闪现靶分数应为 150"
    print("✓ FlickTarget 测试通过")
    
    # 测试追踪靶
    tt = TrackingTarget(300, 300, 40, (0, 0, 255), speed=100, amplitude=50)
    initial_x = tt.x
    tt.update(0.1)
    assert tt.x != initial_x or tt.y != tt.y, "追踪靶应该移动"
    assert tt.get_score() == 200, "追踪靶分数应为 200"
    print("✓ TrackingTarget 测试通过")
    
    print("-" * 50)
    print("目标系统测试完成\n")


def test_data_tracking():
    """测试数据追踪"""
    print("\n[测试 2] 数据追踪系统")
    print("-" * 50)
    
    from data_tracker import DataTracker
    
    dt = DataTracker()
    dt.start_session()
    
    # 记录一些测试数据
    for i in range(10):
        dt.record_click(
            mouse_x=100 + i * 50,
            mouse_y=200,
            target_center=(150 + i * 50, 200),
            hit=(i % 2 == 0)
        )
    
    clicks = dt.get_clicks()
    assert len(clicks) == 10, f"应该有 10 次点击记录，实际{len(clicks)}"
    
    hits = dt.get_hits()
    misses = dt.get_misses()
    assert len(hits) == 5, f"应该有 5 次命中，实际{len(hits)}"
    assert len(misses) == 5, f"应该有 5 次未命中，实际{len(misses)}"
    
    print(f"✓ 数据追踪测试通过 (总点击：{len(clicks)}, 命中：{len(hits)}, 未命中：{len(misses)})")
    print("-" * 50)
    print("数据追踪系统测试完成\n")


def test_data_analysis():
    """测试数据分析"""
    print("\n[测试 3] 数据分析系统")
    print("-" * 50)
    
    from data_tracker import DataTracker
    from data_analyzer import DataAnalyzer
    
    dt = DataTracker()
    dt.start_session()
    
    # 模拟游戏数据
    base_time = time.time()
    for i in range(20):
        dt.clicks.append({
            'timestamp': i * 0.5,
            'mouse_x': 500 + i * 10,
            'mouse_y': 400,
            'target_x': 500 + i * 10,
            'target_y': 400,
            'hit': i % 3 != 0,
            'session_id': dt.session_id
        })
    
    analyzer = DataAnalyzer(dt)
    analyzer.process_data()
    metrics = analyzer.get_metrics()
    
    assert metrics['total_clicks'] == 20, "总点击数应为 20"
    assert metrics['hits'] == 14, "命中数应为 14"
    assert metrics['misses'] == 6, "未命中数应为 6"
    assert 65 < metrics['accuracy'] < 75, f"命中率应在 70% 左右，实际{metrics['accuracy']}"
    
    print(f"✓ 数据分析测试通过")
    print(f"  - 总点击：{metrics['total_clicks']}")
    print(f"  - 命中率：{metrics['accuracy']:.1f}%")
    print(f"  - 平均 TTK: {metrics['avg_ttk']:.1f}ms")
    print(f"  - 平均偏移：{metrics['avg_offset']:.1f}px")
    print("-" * 50)
    print("数据分析系统测试完成\n")


def test_visualization():
    """测试数据可视化"""
    print("\n[测试 4] 数据可视化系统")
    print("-" * 50)
    
    from data_tracker import DataTracker
    from data_analyzer import DataAnalyzer
    from data_visualizer import DataVisualizer
    
    dt = DataTracker()
    dt.start_session()
    
    # 生成测试数据
    import random
    for i in range(50):
        hit = random.random() > 0.3
        dt.clicks.append({
            'timestamp': i * 0.3,
            'mouse_x': random.randint(0, 1920),
            'mouse_y': random.randint(0, 1080),
            'target_x': random.randint(0, 1920) if hit else None,
            'target_y': random.randint(0, 1080) if hit else None,
            'hit': hit,
            'session_id': dt.session_id
        })
    
    analyzer = DataAnalyzer(dt)
    analyzer.process_data()
    
    visualizer = DataVisualizer(analyzer)
    
    # 测试图表生成
    heatmap_path = visualizer.create_heatmap('test_heatmap.png')
    assert heatmap_path is not None, "热力图生成失败"
    print(f"✓ 热力图生成成功：{heatmap_path}")
    
    reaction_path = visualizer.create_reaction_time_plot('test_reaction.png')
    assert reaction_path is not None, "反应时间图生成失败"
    print(f"✓ 反应时间图生成成功：{reaction_path}")
    
    accuracy_path = visualizer.create_accuracy_pie('test_accuracy.png')
    assert accuracy_path is not None, "命中率饼图生成失败"
    print(f"✓ 命中率饼图生成成功：{accuracy_path}")
    
    print("-" * 50)
    print("数据可视化系统测试完成\n")


def test_report_generation():
    """测试报告生成"""
    print("\n[测试 5] 报告生成系统")
    print("-" * 50)
    
    from data_tracker import DataTracker
    from data_analyzer import DataAnalyzer
    from data_visualizer import DataVisualizer
    from report_generator import ReportGenerator
    
    # 准备测试数据
    dt = DataTracker()
    dt.start_session()
    
    import random
    for i in range(30):
        hit = random.random() > 0.4
        dt.clicks.append({
            'timestamp': i * 0.4,
            'mouse_x': random.randint(0, 1920),
            'mouse_y': random.randint(0, 1080),
            'target_x': random.randint(0, 1920) if hit else None,
            'target_y': random.randint(0, 1080) if hit else None,
            'hit': hit,
            'session_id': dt.session_id
        })
    
    analyzer = DataAnalyzer(dt)
    analyzer.process_data()
    
    visualizer = DataVisualizer(analyzer)
    visualizer.create_heatmap()
    visualizer.create_reaction_time_plot()
    visualizer.create_accuracy_pie()
    
    report_gen = ReportGenerator(analyzer, visualizer)
    report_path = report_gen.create_report('TestPlayer')
    
    assert report_path is not None, "报告生成失败"
    print(f"✓ Word 报告生成成功：{report_path}")
    print("-" * 50)
    print("报告生成系统测试完成\n")


def test_config():
    """测试配置文件"""
    print("\n[测试 6] 配置文件")
    print("-" * 50)
    
    from config import (
        SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
        INITIAL_LIVES, GAME_DURATION, TARGET_SPAWN_RATE,
        SCORE_HIT, SCORE_MISS, SCORE_HEADSHOT
    )
    
    assert SCREEN_WIDTH > 0 and SCREEN_HEIGHT > 0, "分辨率设置错误"
    assert FPS > 0, "帧率设置错误"
    assert INITIAL_LIVES > 0, "初始生命值设置错误"
    assert GAME_DURATION > 0, "游戏时长设置错误"
    assert TARGET_SPAWN_RATE > 0, "生成速率设置错误"
    
    print(f"✓ 配置文件测试通过")
    print(f"  - 分辨率：{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"  - 帧率：{FPS} FPS")
    print(f"  - 游戏时长：{GAME_DURATION}秒")
    print(f"  - 生成速率：{TARGET_SPAWN_RATE} 个/秒")
    print("-" * 50)
    print("配置文件测试完成\n")


def main():
    """主函数"""
    print("=" * 60)
    print("Aim Lab 练枪模拟器 - 完整功能测试")
    print("=" * 60)
    
    tests = [
        test_config,
        test_target_system,
        test_data_tracking,
        test_data_analysis,
        test_visualization,
        test_report_generation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n✗ 测试失败：{e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("=" * 60)
    print(f"测试结果：{passed} 通过，{failed} 失败")
    print("=" * 60)
    
    if failed == 0:
        print("\n✓ 所有测试通过！系统运行正常。")
        print("\n下一步:")
        print("1. 运行游戏：python main.py")
        print("2. 查看生成的报告：reports/ 目录")
        print("3. 查看示例图表：reports/*.png")
        return 0
    else:
        print(f"\n✗ 有 {failed} 个测试失败，请检查错误信息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
