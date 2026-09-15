"""
Crosshair 类 - 支持多种准星风格
类似 CS2 5E 平台的准星系统
作者学号：请在此处填写你的学号
"""
import pygame


class CrosshairStyle:
    """准星风格枚举"""
    DOT = 0           # 点
    CROSS = 1         # 十字形
    CIRCLE = 2        # 圆形
    CROSSHAIR = 3     # 传统准星（十字 + 圆）
    T_SHAPE = 4       # T 字形
    SQUARE = 5        # 方形
    DIAMOND = 6       # 菱形
    TRIANGLE = 7      # 三角形


class Crosshair:
    """自定义准星类 - 支持多种风格"""
    
    def __init__(self, style=CrosshairStyle.CROSSHAIR):
        """
        初始化准星
        
        参数:
            style: 准星风格（默认十字 + 圆）
        """
        self.x = 0
        self.y = 0
        self.style = style
        self.smooth_factor = 1.0  # 【修复】1:1 无延迟原生输入
        
        # 准星参数
        self.size = 20          # 准星大小
        self.thickness = 2      # 线条粗细
        self.gap = 3            # 中心间隔（十字形用）
        self.dot_size = 4       # 点大小
        self.color = (0, 255, 0)      # 绿色
        self.inner_color = (255, 0, 0)  # 红色中心点
        self.outer_color = (0, 255, 0)  # 外圈颜色
        
        # 准星预设（类似 CS2 5E 平台）
        self.presets = {
            'default': {
                'style': CrosshairStyle.CROSSHAIR,
                'size': 20,
                'thickness': 2,
                'gap': 3,
                'color': (0, 255, 0),
                'inner_color': (255, 0, 0)
            },
            'dot': {
                'style': CrosshairStyle.DOT,
                'size': 4,
                'thickness': 2,
                'gap': 0,
                'color': (0, 255, 0),
                'inner_color': (255, 255, 255)
            },
            'cross': {
                'style': CrosshairStyle.CROSS,
                'size': 25,
                'thickness': 3,
                'gap': 5,
                'color': (0, 255, 0),
                'inner_color': (0, 0, 0)
            },
            'circle': {
                'style': CrosshairStyle.CIRCLE,
                'size': 15,
                'thickness': 2,
                'gap': 0,
                'color': (255, 255, 0),
                'inner_color': (255, 0, 0)
            },
            't_shape': {
                'style': CrosshairStyle.T_SHAPE,
                'size': 20,
                'thickness': 2,
                'gap': 0,
                'color': (0, 255, 255),
                'inner_color': (255, 0, 255)
            },
            'square': {
                'style': CrosshairStyle.SQUARE,
                'size': 15,
                'thickness': 2,
                'gap': 3,
                'color': (255, 0, 255),
                'inner_color': (0, 255, 255)
            },
            'diamond': {
                'style': CrosshairStyle.DIAMOND,
                'size': 18,
                'thickness': 2,
                'gap': 0,
                'color': (255, 255, 255),
                'inner_color': (255, 0, 0)
            },
            'triangle': {
                'style': CrosshairStyle.TRIANGLE,
                'size': 20,
                'thickness': 2,
                'gap': 0,
                'color': (255, 165, 0),
                'inner_color': (0, 0, 255)
            }
        }
        
        # 加载默认预设
        self.load_preset('default')
    
    def load_preset(self, preset_name):
        """
        加载准星预设
        
        参数:
            preset_name: 预设名称
        """
        if preset_name in self.presets:
            preset = self.presets[preset_name]
            self.style = preset['style']
            self.size = preset['size']
            self.thickness = preset['thickness']
            self.gap = preset['gap']
            self.color = preset['color']
            self.inner_color = preset['inner_color']
    
    def set_style(self, style):
        """
        设置准星风格
        
        参数:
            style: CrosshairStyle 枚举值
        """
        self.style = style
    
    def next_style(self):
        """切换到下一个准星风格并重载参数"""
        self.style = (self.style + 1) % 8
        
        # 建立映射字典
        style_to_preset = {
            CrosshairStyle.DOT: 'dot',
            CrosshairStyle.CROSS: 'cross',
            CrosshairStyle.CIRCLE: 'circle',
            CrosshairStyle.CROSSHAIR: 'default',
            CrosshairStyle.T_SHAPE: 't_shape',
            CrosshairStyle.SQUARE: 'square',
            CrosshairStyle.DIAMOND: 'diamond',
            CrosshairStyle.TRIANGLE: 'triangle'
        }
        
        preset_name = style_to_preset.get(self.style, 'default')
        self.load_preset(preset_name)
    
    def prev_style(self):
        """切换到上一个准星风格并重载参数"""
        self.style = (self.style - 1) % 8
        
        # 建立映射字典
        style_to_preset = {
            CrosshairStyle.DOT: 'dot',
            CrosshairStyle.CROSS: 'cross',
            CrosshairStyle.CIRCLE: 'circle',
            CrosshairStyle.CROSSHAIR: 'default',
            CrosshairStyle.T_SHAPE: 't_shape',
            CrosshairStyle.SQUARE: 'square',
            CrosshairStyle.DIAMOND: 'diamond',
            CrosshairStyle.TRIANGLE: 'triangle'
        }
        
        preset_name = style_to_preset.get(self.style, 'default')
        self.load_preset(preset_name)
    
    def update(self, mouse_x, mouse_y):
        """
        更新准星位置，平滑跟随鼠标
        
        参数:
            mouse_x: 鼠标 X 坐标
            mouse_y: 鼠标 Y 坐标
        """
        self.x += (mouse_x - self.x) * self.smooth_factor
        self.y += (mouse_y - self.y) * self.smooth_factor
    
    def draw(self, screen):
        """
        在屏幕上绘制准星
        
        参数:
            screen: pygame 显示表面
        """
        center_x = int(self.x)
        center_y = int(self.y)
        
        if self.style == CrosshairStyle.DOT:
            self._draw_dot(screen, center_x, center_y)
        elif self.style == CrosshairStyle.CROSS:
            self._draw_cross(screen, center_x, center_y)
        elif self.style == CrosshairStyle.CIRCLE:
            self._draw_circle(screen, center_x, center_y)
        elif self.style == CrosshairStyle.CROSSHAIR:
            self._draw_crosshair(screen, center_x, center_y)
        elif self.style == CrosshairStyle.T_SHAPE:
            self._draw_t_shape(screen, center_x, center_y)
        elif self.style == CrosshairStyle.SQUARE:
            self._draw_square(screen, center_x, center_y)
        elif self.style == CrosshairStyle.DIAMOND:
            self._draw_diamond(screen, center_x, center_y)
        elif self.style == CrosshairStyle.TRIANGLE:
            self._draw_triangle(screen, center_x, center_y)
    
    def _draw_dot(self, screen, cx, cy):
        """绘制点状准星"""
        pygame.draw.circle(screen, self.color, (cx, cy), self.dot_size)
    
    def _draw_cross(self, screen, cx, cy):
        """绘制十字形准星"""
        half = self.size // 2
        
        # 横线
        pygame.draw.line(screen, self.color, 
                        (cx - half - self.gap, cy), 
                        (cx - self.gap, cy), 
                        self.thickness)
        pygame.draw.line(screen, self.color, 
                        (cx + self.gap, cy), 
                        (cx + half + self.gap, cy), 
                        self.thickness)
        
        # 竖线
        pygame.draw.line(screen, self.color, 
                        (cx, cy - half - self.gap), 
                        (cx, cy - self.gap), 
                        self.thickness)
        pygame.draw.line(screen, self.color, 
                        (cx, cy + self.gap), 
                        (cx, cy + half + self.gap), 
                        self.thickness)
    
    def _draw_circle(self, screen, cx, cy):
        """绘制圆形准星"""
        pygame.draw.circle(screen, self.color, (cx, cy), self.size, self.thickness)
        pygame.draw.circle(screen, self.inner_color, (cx, cy), 3)
    
    def _draw_crosshair(self, screen, cx, cy):
        """绘制传统准星（十字 + 圆）"""
        # 外圆
        pygame.draw.circle(screen, self.color, (cx, cy), self.size, 2)
        
        # 十字线
        pygame.draw.line(screen, self.color, 
                        (cx - self.size, cy), 
                        (cx + self.size, cy), 
                        1)
        pygame.draw.line(screen, self.color, 
                        (cx, cy - self.size), 
                        (cx, cy + self.size), 
                        1)
        
        # 中心点
        pygame.draw.circle(screen, self.inner_color, (cx, cy), 3)
    
    def _draw_t_shape(self, screen, cx, cy):
        """绘制 T 字形准星"""
        half = self.size // 2
        
        # 上横线
        pygame.draw.line(screen, self.color, 
                        (cx - half, cy - half), 
                        (cx + half, cy - half), 
                        self.thickness)
        
        # 下竖线
        pygame.draw.line(screen, self.color, 
                        (cx, cy - half), 
                        (cx, cy + half), 
                        self.thickness)
        
        # 中心点
        pygame.draw.circle(screen, self.inner_color, (cx, cy), 3)
    
    def _draw_square(self, screen, cx, cy):
        """绘制方形准星"""
        half = self.size // 2
        rect = pygame.Rect(cx - half, cy - half, self.size, self.size)
        pygame.draw.rect(screen, self.color, rect, self.thickness)
        pygame.draw.circle(screen, self.inner_color, (cx, cy), 3)
    
    def _draw_diamond(self, screen, cx, cy):
        """绘制菱形准星"""
        half = self.size // 2
        points = [
            (cx, cy - half),      # 上
            (cx + half, cy),      # 右
            (cx, cy + half),      # 下
            (cx - half, cy)       # 左
        ]
        pygame.draw.polygon(screen, self.color, points, self.thickness)
        pygame.draw.circle(screen, self.inner_color, (cx, cy), 3)
    
    def _draw_triangle(self, screen, cx, cy):
        """绘制三角形准星"""
        half = self.size // 2
        points = [
            (cx, cy - half),          # 上顶点
            (cx + half, cy + half),   # 右下
            (cx - half, cy + half)    # 左下
        ]
        pygame.draw.polygon(screen, self.color, points, self.thickness)
        pygame.draw.circle(screen, self.inner_color, (cx, cy), 3)
    
    def get_position(self):
        """获取准星当前位置"""
        return (self.x, self.y)
    
    def get_style_name(self):
        """获取当前准星风格名称"""
        style_names = {
            CrosshairStyle.DOT: 'Dot',
            CrosshairStyle.CROSS: 'Cross',
            CrosshairStyle.CIRCLE: 'Circle',
            CrosshairStyle.CROSSHAIR: 'Classic',
            CrosshairStyle.T_SHAPE: 'T-Shape',
            CrosshairStyle.SQUARE: 'Square',
            CrosshairStyle.DIAMOND: 'Diamond',
            CrosshairStyle.TRIANGLE: 'Triangle'
        }
        return style_names.get(self.style, 'Unknown')
