"""
项目配置文件
包含游戏常量、路径配置等
"""
import os

# ========================================
# 🎨 终极科技风调色板 (RGB) - 参考 Valorant/CS2/Osu
# ========================================

# 背景色：深邃宇宙黑
BG_COLOR = (10, 12, 16)
BG_GRADIENT_START = (10, 12, 16)      # 顶部渐变
BG_GRADIENT_END = (20, 25, 35)        # 底部渐变
GRID_COLOR = (30, 40, 55)             # 网格线
GRID_SECONDARY = (40, 55, 75)         # 次要网格

# 靶子配色 (赛博荧光系 - 超高对比度)
TARGET_COLORS = {
    'normal': (0, 212, 255),   # 极光蓝 (普通靶)
    'flick': (255, 46, 147),   # 霓虹粉 (闪现靶)
    'tracking': (255, 215, 0), # 电竞黄 (追踪靶)
    'headshot': (255, 51, 51)  # 警戒红 (爆头靶)
}

# 特效颜色
EFFECT_COLORS = {
    'hit_marker': (255, 255, 255),      # 白色命中提示
    'headshot_glow': (255, 215, 0),     # 金色爆头光晕
    'combo': (0, 255, 255),             # 青色连击
    'rank_up': (255, 215, 0),           # 金色升级
    'particle_blue': (0, 212, 255),     # 蓝色粒子
    'particle_pink': (255, 46, 147),    # 粉色粒子
    'particle_gold': (255, 215, 0),     # 金色粒子
}

# UI 配色 (现代渐变风格)
UI_TEXT_COLOR = (240, 245, 250)
UI_PANEL_BG = (15, 20, 28, 200)
UI_ACCENT_COLOR = (0, 212, 255)         # 极光蓝
UI_GRADIENT_START = (0, 212, 255)       # 渐变起始
UI_GRADIENT_END = (0, 100, 255)         # 渐变结束
UI_HIGHLIGHT = (255, 255, 255)          # 高亮白
UI_DANGER = (255, 80, 80)               # 危险红
UI_SUCCESS = (0, 255, 150)              # 成功绿

# 评级颜色
RANK_COLORS = {
    'S+': (255, 215, 0),      # 金色
    'S': (255, 223, 50),
    'A+': (191, 64, 191),     # 紫色
    'A': (200, 80, 200),
    'B+': (0, 191, 255),      # 蓝色
    'B': (0, 200, 255),
    'C+': (255, 165, 0),      # 橙色
    'C': (255, 180, 0),
    'D': (255, 100, 100),     # 红色
    'F': (128, 128, 128),     # 灰色
}

# 准星颜色
CROSSHAIR_COLORS = {
    'green': (0, 255, 0),      # 经典绿
    'cyan': (0, 255, 255),     # 青色
    'red': (255, 0, 0),        # 红色
    'white': (255, 255, 255),  # 白色
    'yellow': (255, 255, 0),   # 黄色
    'pink': (255, 46, 147),    # 粉色
    'gold': (255, 215, 0),     # 金色
}

# ========================================
# 屏幕设置
# ========================================
# 可以根据你的显示器分辨率调整
# 常见分辨率：1920x1080, 1600x900, 1366x768, 1280x720
# 窗口模式推荐：1280x720 或 1024x768
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 120

# 窗口模式设置（如需窗口模式，取消下面两行的注释）
# SCREEN_WIDTH = 1280
# SCREEN_HEIGHT = 720
# 并在 game_manager.py 中修改：pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# ========================================
# 游戏设置
# ========================================
INITIAL_LIVES = 3
GAME_DURATION = 60  # 游戏时长（秒）
TARGET_SPAWN_RATE = 1.0  # 每秒生成靶子数量
MAX_TARGETS = 4  # 同屏最大靶子数（CS2 模式）

# ========================================
# 计分设置
# ========================================
SCORE_HIT = 100
SCORE_MISS = -50
SCORE_HEADSHOT = 200

# ========================================
# 靶子尺寸设置（可根据屏幕大小调整）
# ========================================
# 小屏幕（1280x720）：20-35
# 中屏幕（1600x900）：25-45
# 大屏幕（1920x1080）：30-50
TARGET_RADIUS_MIN = 20  # 最小半径
TARGET_RADIUS_MAX = 35  # 最大半径

# ========================================
# 路径设置
# ========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 确保目录存在
for directory in [ASSETS_DIR, REPORTS_DIR, DATA_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)
