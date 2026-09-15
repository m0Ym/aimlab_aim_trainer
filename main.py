"""
Aim Lab 练枪模拟器 - 主程序入口
终极科技风版本 - 参考 Valorant/CS2/Osu 设计
作者：请在此处填写小组成员姓名
学号：请在此处填写学号
创建日期：2026-05-26
"""
from game_manager_modern import GameManager


def main():
    """主函数"""
    print("=" * 60)
    print("Aim Lab - Ultimate Tech Edition")
    print("=" * 60)
    print("\n操作说明:")
    print("- 移动鼠标控制准星")
    print("- 点击鼠标左键射击")
    print("- 按 SPACE 开始游戏")
    print("- 按 C 键切换准星")
    print("- 按 ESC 退出游戏")
    print("=" * 60)
    
    game = GameManager()
    game.run()


if __name__ == "__main__":
    main()
