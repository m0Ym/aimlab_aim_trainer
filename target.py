"""
Target 基类 - 组员 C 负责
定义目标的基本属性和行为
作者学号：请在此处填写你的学号
"""
import pygame
import math


class Target:
    """目标基类，所有靶子类型的父类"""
    
    def __init__(self, x, y, radius, color):
        """
        初始化目标
        
        参数:
            x: 横坐标
            y: 纵坐标
            radius: 半径
            color: 颜色 (RGB 三元组)
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.is_alive = True
        self.spawn_time = pygame.time.get_ticks()
    
    def draw(self, screen):
        """
        在屏幕上绘制目标（电竞风格：发光边缘 + 立体感）
        
        参数:
            screen: pygame 显示表面
        """
        if not self.is_alive:
            return
        
        x, y = int(self.x), int(self.y)
        
        # 1. 绘制暗色外发光/阴影层 (稍微大一点)
        pygame.draw.circle(screen, (10, 10, 10), (x, y), self.radius + 2)
        
        # 2. 绘制主颜色层
        pygame.draw.circle(screen, self.color, (x, y), self.radius)
        
        # 3. 绘制内圈渐变 (立体感)
        # 将主色调变暗 30% 作为内圈
        darker_color = (max(0, self.color[0]-60), max(0, self.color[1]-60), max(0, self.color[2]-60))
        inner_radius = max(5, self.radius - 4)
        pygame.draw.circle(screen, darker_color, (x, y), inner_radius)
        
        # 4. 绘制高对比度靶心（白色圆点）
        center_radius = max(3, self.radius // 4)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), center_radius)
        
        # 5. 绘制白色外边框
        pygame.draw.circle(screen, (255, 255, 255), (x, y), self.radius, 2)
    
    def check_click(self, mouse_x, mouse_y):
        """
        检查鼠标点击是否击中目标
        
        使用勾股定理计算距离
        返回布尔值表示是否击中
        
        参数:
            mouse_x: 鼠标点击的 X 坐标
            mouse_y: 鼠标点击的 Y 坐标
            
        返回:
            bool: True 表示击中，False 表示未击中
        """
        if not self.is_alive:
            return False
        
        distance = math.sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2)
        return distance <= self.radius
    
    def get_center(self):
        """获取目标中心坐标"""
        return (self.x, self.y)
    
    def destroy(self):
        """销毁目标"""
        self.is_alive = False
    
    def update(self, delta_time):
        """
        更新目标状态（基类为空实现，由子类重写）
        
        参数:
            delta_time: 距离上一帧的时间间隔（秒）
        """
        pass
    
    def get_score(self):
        """获取击杀此目标的分数（基类返回 100）"""
        return 100
