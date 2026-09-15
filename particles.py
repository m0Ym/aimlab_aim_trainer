"""
粒子系统 - 现代科技风格特效
用于菜单背景、命中特效、连击动画等
"""
import pygame
import random
import math


class Particle:
    """单个粒子"""
    
    def __init__(self, x, y, color, velocity=None, lifetime=2000, size=3):
        """
        初始化粒子
        
        参数:
            x, y: 初始位置
            color: 颜色 (RGB)
            velocity: 速度向量 (vx, vy)
            lifetime: 存活时间 (毫秒)
            size: 粒子大小
        """
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity or (random.uniform(-2, 2), random.uniform(-2, 2))
        self.lifetime = lifetime
        self.size = size
        self.spawn_time = pygame.time.get_ticks()
        self.alpha = 255
        self.decay = random.uniform(0.5, 1.0)  # 衰减速度
    
    def update(self):
        """更新粒子状态"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.spawn_time
        
        # 移动
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        # 计算透明度
        progress = elapsed / self.lifetime
        self.alpha = max(0, int(255 * (1 - progress) * self.decay))
        
        return elapsed < self.lifetime
    
    def draw(self, screen):
        """绘制粒子"""
        if self.alpha <= 0:
            return
        
        # 创建支持透明度的表面
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        # 绘制发光粒子
        color_with_alpha = (*self.color, self.alpha)
        pygame.draw.circle(particle_surface, color_with_alpha, (self.size, self.size), self.size)
        
        screen.blit(particle_surface, (int(self.x) - self.size, int(self.y) - self.size), 
                   special_flags=pygame.BLEND_RGBA_ADD)


class ParticleSystem:
    """粒子系统管理器"""
    
    def __init__(self):
        """初始化粒子系统"""
        self.particles = []
    
    def emit(self, x, y, color, count=10, velocity_range=None, lifetime=2000, size=3):
        """
        发射粒子
        
        参数:
            x, y: 发射位置
            color: 颜色
            count: 粒子数量
            velocity_range: 速度范围
            lifetime: 存活时间
            size: 粒子大小
        """
        for _ in range(count):
            if velocity_range:
                vx = random.uniform(-velocity_range, velocity_range)
                vy = random.uniform(-velocity_range, velocity_range)
                velocity = (vx, vy)
            else:
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 5)
                velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            
            particle = Particle(x, y, color, velocity, lifetime, size)
            self.particles.append(particle)
    
    def emit_explosion(self, x, y, color, count=30):
        """发射爆炸效果"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            particle = Particle(x, y, color, velocity, lifetime=1500, size=random.randint(2, 5))
            self.particles.append(particle)
    
    def emit_trail(self, x, y, color, count=5):
        """发射拖尾效果"""
        for _ in range(count):
            velocity = (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
            particle = Particle(x, y, color, velocity, lifetime=300, size=random.randint(1, 3))
            self.particles.append(particle)
    
    def update(self):
        """更新所有粒子"""
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self, screen):
        """绘制所有粒子"""
        for particle in self.particles:
            particle.draw(screen)
    
    def clear(self):
        """清空所有粒子"""
        self.particles = []


class FloatingText:
    """浮动文字效果（伤害数字、连击数等）"""
    
    def __init__(self, x, y, text, color, font_size=36, lifetime=1000, velocity=(0, -2)):
        """
        初始化浮动文字
        
        参数:
            x, y: 位置
            text: 文字内容
            color: 颜色
            font_size: 字体大小
            lifetime: 存活时间
            velocity: 移动速度
        """
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.lifetime = lifetime
        self.velocity = velocity
        self.spawn_time = pygame.time.get_ticks()
        self.alpha = 255
        self.scale = 1.0
    
    def update(self):
        """更新文字状态"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.spawn_time
        
        # 移动
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        # 计算透明度和缩放
        progress = elapsed / self.lifetime
        self.alpha = max(0, int(255 * (1 - progress)))
        self.scale = max(0.5, 1.0 - progress * 0.3)
        
        return elapsed < self.lifetime
    
    def draw(self, screen):
        """绘制浮动文字"""
        if self.alpha <= 0:
            return
        
        # 渲染文字
        text_surface = self.font.render(self.text, True, self.color)
        
        # 缩放
        if self.scale != 1.0:
            new_size = (int(text_surface.get_width() * self.scale), 
                       int(text_surface.get_height() * self.scale))
            text_surface = pygame.transform.scale(text_surface, new_size)
        
        # 设置透明度
        text_surface.set_alpha(self.alpha)
        
        # 绘制
        rect = text_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text_surface, rect)
