"""
打包脚本 - 准备最终提交材料
"""
import os
import shutil
from datetime import datetime


def create_submission_package():
    """创建提交包"""
    print("=" * 60)
    print("Aim Lab 练枪模拟器 - 打包提交材料")
    print("=" * 60)
    
    # 获取当前日期
    today = datetime.now().strftime("%Y%m%d")
    
    # 基础目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    package_name = f"研修报告 - 小组-{today}"
    package_dir = os.path.join(base_dir, package_name)
    
    # 如果已存在，删除旧包
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
        print(f"✓ 删除旧包：{package_name}")
    
    # 创建新包目录
    os.makedirs(package_dir)
    os.makedirs(os.path.join(package_dir, "源代码"))
    os.makedirs(os.path.join(package_dir, "reports"))
    os.makedirs(os.path.join(package_dir, "data"))
    os.makedirs(os.path.join(package_dir, "照片"))
    os.makedirs(os.path.join(package_dir, "视频"))
    
    print(f"✓ 创建包目录：{package_name}")
    
    # 复制源代码文件
    source_files = [
        'main.py',
        'config.py',
        'game_manager.py',
        'target.py',
        'target_types.py',
        'crosshair.py',
        'data_tracker.py',
        'data_analyzer.py',
        'data_visualizer.py',
        'report_generator.py',
        'requirements.txt',
        'README.md',
        'AI 使用说明.txt',
        '研修报告模板.md',
        'test_imports.py',
        'test_full.py',
        'run.bat'
    ]
    
    for file in source_files:
        src = os.path.join(base_dir, file)
        dst = os.path.join(package_dir, "源代码", file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"✓ 复制源代码：{file}")
        else:
            print(f"⚠ 文件不存在：{file}")
    
    # 复制生成的报告
    reports_dir = os.path.join(base_dir, "reports")
    if os.path.exists(reports_dir):
        for file in os.listdir(reports_dir):
            if file.endswith(('.docx', '.png', '.csv')):
                src = os.path.join(reports_dir, file)
                dst = os.path.join(package_dir, "reports", file)
                shutil.copy2(src, dst)
                print(f"✓ 复制报告文件：{file}")
    
    # 创建说明文件
    readme_content = f"""Aim Lab 练枪模拟器 - 提交材料包
=====================================

提交日期：{datetime.now().strftime("%Y年%m月%d日")}

目录结构：
├── 源代码/           - 完整的源代码文件
├── reports/         - 生成的分析报告和图表
├── data/            - 数据文件
├── 照片/            - 工作照片（限 3 张）
├── 视频/            - 演示视频（限 1 份）
├── 研修报告.pdf      - 研修报告（请手动添加）
└── 说明.txt         - 本文件

提交前检查清单：
□ 研修报告 PDF 已添加
□ 工作照片已添加（不超过 3 张）
□ 演示视频已添加（不超过 1 份）
□ 所有源代码文件已包含
□ 生成的报告样例已包含

命名格式：研修报告 - 组员姓名 - 选题名称 -2026

祝好！
"""
    
    readme_path = os.path.join(package_dir, "说明.txt")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✓ 创建说明文件")
    
    print("\n" + "=" * 60)
    print("打包完成！")
    print("=" * 60)
    print(f"\n包位置：{package_dir}")
    print("\n后续步骤：")
    print("1. 将研修报告 PDF 复制到包目录")
    print("2. 将工作照片复制到 照片/ 目录")
    print("3. 将演示视频复制到 视频/ 目录")
    print("4. 压缩整个包为 ZIP 文件")
    print("5. 发送到指定邮箱")
    
    return package_dir


if __name__ == "__main__":
    create_submission_package()
