"""
地图配置模块
定义不同游戏的地图风格和视觉元素
"""
from enum import Enum


class MapTheme(Enum):
    """地图主题枚举"""
    VALORANT = "valorant"
    CS2 = "cs2"
    OVERWATCH = "overwatch"
    APEX = "apex"
    DEFAULT = "default"


class MapConfig:
    """地图配置类"""
    
    # 默认地图（科技风）
    DEFAULT = {
        'name': 'Tech Lab',
        'theme': MapTheme.DEFAULT,
        'bg_gradient_start': (10, 12, 16),
        'bg_gradient_end': (20, 25, 35),
        'grid_color': (30, 40, 55),
        'grid_secondary': (40, 55, 75),
        'accent_color': (0, 212, 255),
        'target_colors': {
            'normal': (0, 212, 255),   # 极光蓝
            'flick': (255, 46, 147),   # 霓虹粉
            'tracking': (255, 215, 0), # 电竞黄
            'headshot': (255, 51, 51)  # 警戒红
        },
        'particle_color': (0, 212, 255),
        'ui_gradient_start': (0, 212, 255),
        'ui_gradient_end': (0, 100, 255),
        'description': 'Default tech-style training room'
    }
    
    # 瓦洛兰特地图
    VALORANT = {
        'name': 'Valorant Range',
        'theme': MapTheme.VALORANT,
        'bg_gradient_start': (15, 10, 20),
        'bg_gradient_end': (35, 15, 30),
        'grid_color': (50, 30, 50),
        'grid_secondary': (70, 40, 70),
        'accent_color': (255, 70, 70),  # 瓦洛兰特红
        'target_colors': {
            'normal': (255, 70, 70),    # 红色
            'flick': (255, 240, 60),    # 黄色
            'tracking': (60, 255, 180), # 青色
            'headshot': (255, 255, 255) # 白色
        },
        'particle_color': (255, 70, 70),
        'ui_gradient_start': (255, 70, 70),
        'ui_gradient_end': (200, 50, 50),
        'description': 'Valorant-style training range'
    }
    
    # CS2 地图
    CS2 = {
        'name': 'CS2 Training',
        'theme': MapTheme.CS2,
        'bg_gradient_start': (20, 25, 30),
        'bg_gradient_end': (40, 50, 60),
        'grid_color': (60, 70, 80),
        'grid_secondary': (80, 90, 100),
        'accent_color': (100, 200, 255),  # CS2 蓝色
        'target_colors': {
            'normal': (100, 200, 255),    # 蓝色
            'flick': (255, 200, 50),      # 橙色
            'tracking': (100, 255, 100),  # 绿色
            'headshot': (255, 50, 50)     # 红色
        },
        'particle_color': (100, 200, 255),
        'ui_gradient_start': (100, 200, 255),
        'ui_gradient_end': (50, 150, 255),
        'description': 'CS2-style training ground'
    }
    
    # 守望先锋地图
    OVERWATCH = {
        'name': 'Overwatch PTE',
        'theme': MapTheme.OVERWATCH,
        'bg_gradient_start': (255, 180, 50),
        'bg_gradient_end': (255, 200, 100),
        'grid_color': (255, 220, 100),
        'grid_secondary': (255, 230, 120),
        'accent_color': (255, 200, 50),  # 守望橙
        'target_colors': {
            'normal': (255, 200, 50),    # 橙色
            'flick': (0, 200, 255),      # 蓝色
            'tracking': (255, 100, 100), # 红色
            'headshot': (255, 255, 255)  # 白色
        },
        'particle_color': (255, 200, 50),
        'ui_gradient_start': (255, 200, 50),
        'ui_gradient_end': (255, 180, 0),
        'description': 'Overwatch-style practice range'
    }
    
    # Apex 地图
    APEX = {
        'name': 'Apex Firing Range',
        'theme': MapTheme.APEX,
        'bg_gradient_start': (30, 20, 40),
        'bg_gradient_end': (60, 40, 80),
        'grid_color': (80, 60, 100),
        'grid_secondary': (100, 80, 120),
        'accent_color': (200, 50, 100),  # Apex 红粉
        'target_colors': {
            'normal': (200, 50, 100),    # 红粉色
            'flick': (255, 200, 50),     # 金色
            'tracking': (50, 255, 150),  # 绿色
            'headshot': (255, 100, 50)   # 橙色
        },
        'particle_color': (200, 50, 100),
        'ui_gradient_start': (200, 50, 100),
        'ui_gradient_end': (150, 30, 80),
        'description': 'Apex Legends-style firing range'
    }


def get_map_config(map_theme: MapTheme) -> dict:
    """获取地图配置"""
    map_configs = {
        MapTheme.DEFAULT: MapConfig.DEFAULT,
        MapTheme.VALORANT: MapConfig.VALORANT,
        MapTheme.CS2: MapConfig.CS2,
        MapTheme.OVERWATCH: MapConfig.OVERWATCH,
        MapTheme.APEX: MapConfig.APEX,
    }
    return map_configs.get(map_theme, MapConfig.DEFAULT)


def get_all_maps() -> list:
    """获取所有地图配置列表"""
    return [
        MapConfig.DEFAULT,
        MapConfig.VALORANT,
        MapConfig.CS2,
        MapConfig.OVERWATCH,
        MapConfig.APEX,
    ]


def get_map_by_index(index: int) -> dict:
    """通过索引获取地图配置"""
    maps = get_all_maps()
    if 0 <= index < len(maps):
        return maps[index]
    return MapConfig.DEFAULT
