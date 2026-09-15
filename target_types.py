"""
Target 派生类 - 组员 B 负责
实现多态：FlickTarget（闪现靶）和 TrackingTarget（追踪靶）
作者学号：请在此处填写你的学号
"""
import pygame
import math
from target import Target
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class FlickTarget(Target):
    """闪现靶类 - CS2 模式：静止靶子，中等分值"""
    
    def __init__(self, x, y, radius, color):
        """
        初始化闪现靶（CS2 模式：静止不动）
        
        参数:
            x: 横坐标
            y: 纵坐标
            radius: 半径
            color: 颜色
        """
        super().__init__(x, y, radius, color)
        self.score_value = 150
    
    def update(self, delta_time):
        """
        更新闪现靶状态（CS2 模式：不消失）
        
        参数:
            delta_time: 距离上一帧的时间间隔（秒）
        """
        pass
    
    def get_score(self):
        """获取击杀分数"""
        return self.score_value


class TrackingTarget(Target):
    """追踪靶类 - CS2 模式：静止靶子，高分值"""
    
    def __init__(self, x, y, radius, color):
        """
        初始化追踪靶（CS2 模式：静止不动）
        
        参数:
            x: 横坐标
            y: 纵坐标
            radius: 半径
            color: 颜色
        """
        super().__init__(x, y, radius, color)
        self.score_value = 200
    
    def update(self, delta_time):
        """
        更新追踪靶状态（CS2 模式：不移动）
        
        参数:
            delta_time: 距离上一帧的时间间隔（秒）
        """
        pass
    
    def get_score(self):
        """获取击杀分数"""
        return self.score_value


class HeadshotTarget(Target):
    """爆头靶类 - 小尺寸高分数"""
    
    def __init__(self, x, y, radius=15, color=(255, 255, 0)):
        """
        初始化爆头靶
        
        参数:
            x: 横坐标
            y: 纵坐标
            radius: 半径（默认 15）
            color: 颜色（默认黄色）
        """
        super().__init__(x, y, radius, color)
        self.score_value = 300
    
    def get_score(self):
        """获取击杀分数"""
        return self.score_value
