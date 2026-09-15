"""
现代化游戏管理器 - 终极科技风
包含：动态背景、粒子效果、连击系统、炫酷 UI、多地图支持
"""
import pygame
import random
import math
from enum import Enum
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, INITIAL_LIVES, GAME_DURATION
from config import TARGET_SPAWN_RATE, SCORE_HIT, SCORE_MISS, MAX_TARGETS
from config import TARGET_RADIUS_MIN, TARGET_RADIUS_MAX
from config import BG_COLOR, BG_GRADIENT_START, BG_GRADIENT_END
from config import GRID_COLOR, GRID_SECONDARY
from config import UI_TEXT_COLOR, UI_PANEL_BG, UI_ACCENT_COLOR, UI_GRADIENT_START, UI_GRADIENT_END
from config import UI_HIGHLIGHT, UI_DANGER, UI_SUCCESS
from config import TARGET_COLORS, EFFECT_COLORS, RANK_COLORS
from config import TARGET_COLORS
from target import Target
from crosshair import Crosshair
from target_types import FlickTarget, TrackingTarget, HeadshotTarget
from data_tracker import DataTracker
from data_analyzer import DataAnalyzer
from data_visualizer import DataVisualizer
from report_generator import ReportGenerator
from particles import ParticleSystem, FloatingText
from maps import MapConfig, get_map_config, get_all_maps, MapTheme


class GameState(Enum):
    """游戏状态枚举"""
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3


class GameManager:
    """现代化游戏管理器（终极科技风）"""
    
    def __init__(self):
        """初始化游戏管理器"""
        pygame.init()
        pygame.display.set_caption("Aim Lab - Ultimate Tech Edition")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # 字体
        self.font_large = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.tiny_font = pygame.font.Font(None, 28)
        
        # 地图系统
        self.maps = get_all_maps()
        self.current_map_index = 0
        self.current_map = self.maps[self.current_map_index]
        self.update_map_colors()
        
        # 游戏状态
        self.state = GameState.MENU
        self.crosshair = Crosshair()
        self.targets = []
        self.score = 0
        self.lives = INITIAL_LIVES
        self.game_start_time = 0
        self.spawn_timer = 0
        self.hits = 0
        self.misses = 0
        
        # 连击系统
        self.combo = 0
        self.max_combo = 0
        self.combo_timer = 0
        self.COMBO_TIMEOUT = 2000  # 连击超时时间（毫秒）
        
        # 粒子系统
        self.particle_system = ParticleSystem()
        self.floating_texts = []
        
        # 数据追踪
        self.data_tracker = DataTracker()
        self.rank = None
        self.rank_data = {}
        
        # 动画效果
        self.menu_animation_timer = 0
        self.background_offset = 0
        
        self.running = True
    
    def update_map_colors(self):
        """更新当前地图颜色配置"""
        self.bg_gradient_start = tuple(self.current_map['bg_gradient_start'])
        self.bg_gradient_end = tuple(self.current_map['bg_gradient_end'])
        self.grid_color = tuple(self.current_map['grid_color'])
        self.grid_secondary = tuple(self.current_map['grid_secondary'])
        self.accent_color = tuple(self.current_map['accent_color'])
        self.target_colors = self.current_map['target_colors']
        self.particle_color = tuple(self.current_map['particle_color'])
        self.ui_gradient_start = tuple(self.current_map['ui_gradient_start'])
        self.ui_gradient_end = tuple(self.current_map['ui_gradient_end'])
    
    def next_map(self):
        """切换到下一张地图"""
        self.current_map_index = (self.current_map_index + 1) % len(self.maps)
        self.current_map = self.maps[self.current_map_index]
        self.update_map_colors()
    
    def prev_map(self):
        """切换到上一张地图"""
        self.current_map_index = (self.current_map_index - 1) % len(self.maps)
        self.current_map = self.maps[self.current_map_index]
        self.update_map_colors()
    
    def draw_gradient_background(self):
        """绘制渐变背景"""
        # 创建渐变表面
        gradient_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # 绘制渐变（使用当前地图颜色）
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(self.bg_gradient_start[0] + (self.bg_gradient_end[0] - self.bg_gradient_start[0]) * ratio)
            g = int(self.bg_gradient_start[1] + (self.bg_gradient_end[1] - self.bg_gradient_start[1]) * ratio)
            b = int(self.bg_gradient_start[2] + (self.bg_gradient_end[2] - self.bg_gradient_start[2]) * ratio)
            pygame.draw.line(gradient_surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        self.screen.blit(gradient_surface, (0, 0))
    
    def draw_dynamic_grid(self):
        """绘制动态网格（带光效）"""
        grid_size = 80
        
        # 绘制主网格（使用当前地图颜色）
        for x in range(0, SCREEN_WIDTH, grid_size):
            alpha = int(100 + 50 * math.sin(self.menu_animation_timer * 0.002 + x * 0.1))
            color = (*self.grid_color, alpha)
            line_surface = pygame.Surface((2, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(line_surface, color, (0, 0), (0, SCREEN_HEIGHT), 1)
            self.screen.blit(line_surface, (x, 0))
        
        for y in range(0, SCREEN_HEIGHT, grid_size):
            alpha = int(100 + 50 * math.sin(self.menu_animation_timer * 0.002 + y * 0.1))
            color = (*self.grid_color, alpha)
            line_surface = pygame.Surface((SCREEN_WIDTH, 2), pygame.SRCALPHA)
            pygame.draw.line(line_surface, color, (0, 0), (SCREEN_WIDTH, 0), 1)
            self.screen.blit(line_surface, (0, y))
        
        # 绘制中心十字光效
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # 水平光效
        glow_surface = pygame.Surface((SCREEN_WIDTH, 3), pygame.SRCALPHA)
        for x in range(0, SCREEN_WIDTH, 5):
            alpha = int(150 + 100 * math.sin(self.menu_animation_timer * 0.003 + x * 0.05))
            pygame.draw.line(glow_surface, (*self.grid_secondary, alpha), (x, center_y), (x+5, center_y), 2)
        self.screen.blit(glow_surface, (0, center_y))
        
        # 垂直光效
        glow_surface = pygame.Surface((3, SCREEN_HEIGHT), pygame.SRCALPHA)
        for y in range(0, SCREEN_HEIGHT, 5):
            alpha = int(150 + 100 * math.sin(self.menu_animation_timer * 0.003 + y * 0.05))
            pygame.draw.line(glow_surface, (*self.grid_secondary, alpha), (center_x, y), (center_x, y+5), 2)
        self.screen.blit(glow_surface, (center_x, 0))
    
    def draw_menu(self):
        """绘制主菜单（现代科技风）"""
        self.menu_animation_timer = pygame.time.get_ticks()
        
        # 渐变背景
        self.draw_gradient_background()
        
        # 动态网格
        self.draw_dynamic_grid()
        
        # 粒子背景效果
        if random.random() < 0.3:
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            self.particle_system.emit(x, y, self.particle_color, count=3, 
                                     velocity_range=0.5, lifetime=1000, size=2)
        self.particle_system.update()
        self.particle_system.draw(self.screen)
        
        # 标题（带光晕）
        title_glow = self.font_large.render("AIM LAB", True, self.accent_color)
        title_glow.set_alpha(100)
        title_rect = title_glow.get_rect(center=(SCREEN_WIDTH // 2 + 2, SCREEN_HEIGHT // 3 + 2))
        self.screen.blit(title_glow, title_rect)
        
        title = self.font_large.render("AIM LAB", True, UI_HIGHLIGHT)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title, title_rect)
        
        subtitle = self.small_font.render("ULTIMATE TECH EDITION", True, self.accent_color)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 60))
        self.screen.blit(subtitle, subtitle_rect)
        
        # 地图信息
        map_name = self.current_map['name']
        map_text = self.tiny_font.render(f"MAP: {map_name}", True, UI_TEXT_COLOR)
        map_rect = map_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(map_text, map_rect)
        
        # 开始按钮（纯文字，无框框）
        start_text = self.font.render("PRESS SPACE TO START", True, UI_HIGHLIGHT)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(start_text, start_rect)
        
        # 准星信息（极简风格）
        crosshair_text = f"CROSSHAIR: {self.crosshair.get_style_name()}"
        crosshair_info = self.tiny_font.render(crosshair_text, True, UI_TEXT_COLOR)
        crosshair_rect = crosshair_info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(crosshair_info, crosshair_rect)
        
        # 地图切换提示
        map_switch_y = SCREEN_HEIGHT // 2 + 90
        map_switch_text = self.tiny_font.render("LEFT/RIGHT - Switch Map", True, self.accent_color)
        map_switch_rect = map_switch_text.get_rect(center=(SCREEN_WIDTH // 2, map_switch_y))
        self.screen.blit(map_switch_text, map_switch_rect)
        
        # 按键提示（极简风格 - 无框框）
        key_hints_y = SCREEN_HEIGHT // 2 + 120
        
        # C 键提示
        c_key = self.tiny_font.render("C - Switch Crosshair", True, self.accent_color)
        c_key_rect = c_key.get_rect(center=(SCREEN_WIDTH // 2, key_hints_y))
        self.screen.blit(c_key, c_key_rect)
        
        # ESC 键提示
        esc_key = self.tiny_font.render("ESC - Exit", True, UI_DANGER)
        esc_key_rect = esc_key.get_rect(center=(SCREEN_WIDTH // 2, key_hints_y + 35))
        self.screen.blit(esc_key, esc_key_rect)
    
    def draw_modern_ui(self):
        """绘制现代化 UI 面板"""
        # 顶部面板（渐变）
        panel_height = 60
        panel = pygame.Surface((SCREEN_WIDTH, panel_height), pygame.SRCALPHA)
        
        # 渐变背景（使用当前地图颜色）
        for x in range(SCREEN_WIDTH):
            ratio = x / SCREEN_WIDTH
            r = int(self.ui_gradient_start[0] + (self.ui_gradient_end[0] - self.ui_gradient_start[0]) * ratio)
            g = int(self.ui_gradient_start[1] + (self.ui_gradient_end[1] - self.ui_gradient_start[1]) * ratio)
            b = int(self.ui_gradient_start[2] + (self.ui_gradient_end[2] - self.ui_gradient_start[2]) * ratio)
            pygame.draw.line(panel, (r, g, b, 180), (x, 0), (x, panel_height))
        
        self.screen.blit(panel, (0, 0))
        
        # 左侧装饰线（使用当前地图颜色）
        pygame.draw.line(self.screen, self.accent_color, (0, 0), (0, panel_height), 3)
        
        # 分数
        score_text = self.font.render(f"SCORE: {self.score}", True, UI_HIGHLIGHT)
        score_rect = score_text.get_rect(left=30, centery=panel_height // 2)
        self.screen.blit(score_text, score_rect)
        
        # 生命值（带图标）
        lives_text = self.font.render(f"♥ × {self.lives}", True, (255, 80, 80) if self.lives <= 1 else (0, 255, 150))
        lives_rect = lives_text.get_rect(left=300, centery=panel_height // 2)
        self.screen.blit(lives_text, lives_rect)
        
        # 连击数（如果有连击）
        if self.combo > 1:
            combo_color = self.accent_color
            combo_text = self.font.render(f"COMBO ×{self.combo}", True, combo_color)
            combo_rect = combo_text.get_rect(left=500, centery=panel_height // 2)
            self.screen.blit(combo_text, combo_rect)
            
            # 连击光晕
            combo_glow = self.font.render(f"COMBO ×{self.combo}", True, combo_color)
            combo_glow.set_alpha(100)
            self.screen.blit(combo_glow, (502, panel_height // 2 + 2))
        
        # 右侧时间
        elapsed = (pygame.time.get_ticks() - self.game_start_time) / 1000.0
        time_text = self.font.render(f"TIME: {elapsed:.2f}s", True, UI_ACCENT_COLOR)
        time_rect = time_text.get_rect(right=SCREEN_WIDTH - 30, centery=panel_height // 2)
        self.screen.blit(time_text, time_rect)
    
    def draw_game(self):
        """绘制游戏界面（科技感 HUD）"""
        # 渐变背景
        self.draw_gradient_background()
        
        # 静态网格
        grid_size = 80
        for x in range(0, SCREEN_WIDTH, grid_size):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, grid_size):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)
        
        # 绘制靶子
        for target in self.targets:
            target.draw(self.screen)
        
        # 更新和绘制粒子
        self.particle_system.update()
        self.particle_system.draw(self.screen)
        
        # 绘制 Hit Marker
        for hit_marker in self.hit_markers:
            hit_marker.draw(self.screen)
        
        # 绘制浮动文字
        self.floating_texts = [ft for ft in self.floating_texts if ft.update()]
        for ft in self.floating_texts:
            ft.draw(self.screen)
        
        # 准星
        self.crosshair.draw(self.screen)
        
        # 现代化 UI
        self.draw_modern_ui()
    
    def draw_game_over(self):
        """绘制游戏结束界面（炫酷评级动画）"""
        # 渐变背景
        self.draw_gradient_background()
        
        # 动态网格
        self.draw_dynamic_grid()
        
        # 评级（带光晕和动画）
        rank_color = RANK_COLORS.get(self.rank, UI_HIGHLIGHT)
        
        # 评级光晕
        rank_glow = self.font_large.render(self.rank, True, rank_color)
        rank_glow.set_alpha(100)
        rank_glow = pygame.transform.scale(rank_glow, (rank_glow.get_width() + 20, rank_glow.get_height() + 20))
        rank_rect = rank_glow.get_rect(center=(SCREEN_WIDTH // 2 + 2, SCREEN_HEIGHT // 3 + 2))
        self.screen.blit(rank_glow, rank_rect)
        
        # 评级文字
        rank_text = self.font_large.render(self.rank, True, UI_HIGHLIGHT)
        rank_rect = rank_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(rank_text, rank_rect)
        
        # 评级描述
        rank_desc = self.get_rank_description(self.rank)
        desc_text = self.small_font.render(rank_desc, True, rank_color)
        desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 60))
        self.screen.blit(desc_text, desc_rect)
        
        # 统计项目（无框框，纯文字）
        stats = [
            f"Final Score: {self.score}",
            f"Accuracy: {self.analyzer.metrics['accuracy']:.1f}%",
            f"Avg TTK: {self.analyzer.metrics['avg_ttk']:.1f}ms",
            f"Max Combo: {self.max_combo}",
            f"Hits: {self.hits} | Misses: {self.misses}",
        ]
        
        for i, stat in enumerate(stats):
            stat_text = self.small_font.render(stat, True, UI_TEXT_COLOR)
            stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80 + i * 50))
            self.screen.blit(stat_text, stat_rect)
        
        # 底部提示
        restart_text = self.font.render("SPACE - Restart | ESC - Menu", True, UI_ACCENT_COLOR)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        self.screen.blit(restart_text, restart_rect)
    
    def get_rank_description(self, rank):
        """获取评级描述"""
        descriptions = {
            'S+': 'LEGENDARY - 传奇大师',
            'S': 'GRANDMASTER - 宗师',
            'A+': 'MASTER - 大师',
            'A': 'DIAMOND - 钻石',
            'B+': 'PLATINUM - 白金',
            'B': 'GOLD - 黄金',
            'C+': 'SILVER - 白银',
            'C': 'BRONZE - 青铜',
            'D': 'IRON - 黑铁',
            'F': 'UNRANKED - 未评级',
        }
        return descriptions.get(rank, '')
    
    def handle_click(self):
        """处理鼠标点击（带连击和特效）"""
        if self.state != GameState.PLAYING:
            return
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hit = False
        hit_target = None
        
        for target in self.targets:
            if target.check_click(mouse_x, mouse_y):
                hit = True
                hit_target = target
                self.score += target.get_score()
                self.hits += 1
                
                # 连击系统
                current_time = pygame.time.get_ticks()
                if current_time - self.combo_timer < self.COMBO_TIMEOUT:
                    self.combo += 1
                else:
                    self.combo = 1
                self.combo_timer = current_time
                
                if self.combo > self.max_combo:
                    self.max_combo = self.combo
                
                # Hit Marker 效果
                is_headshot = hasattr(target, 'is_headshot') and target.is_headshot
                self.hit_markers.append(HitMarker(mouse_x, mouse_y, is_headshot))
                
                # 粒子爆炸效果
                if is_headshot:
                    self.particle_system.emit_explosion(mouse_x, mouse_y, self.target_colors['headshot'], count=50)
                    # 浮动文字
                    ft = FloatingText(mouse_x, mouse_y, "HEADSHOT!", self.target_colors['headshot'], 
                                     font_size=48, lifetime=1500, velocity=(0, -3))
                    self.floating_texts.append(ft)
                else:
                    self.particle_system.emit_explosion(mouse_x, mouse_y, self.particle_color, count=30)
                    # 浮动分数
                    ft = FloatingText(mouse_x, mouse_y, f"+{target.get_score()}", self.accent_color, 
                                     font_size=36, lifetime=1000, velocity=(0, -2))
                    self.floating_texts.append(ft)
                
                # 连击浮动文字
                if self.combo >= 5:
                    ft = FloatingText(mouse_x, mouse_y, f"COMBO ×{self.combo}!", self.accent_color, 
                                     font_size=42, lifetime=1200, velocity=(0, -2.5))
                    self.floating_texts.append(ft)
                
                target.destroy()
                break
        
        if hit:
            self.data_tracker.record_click(mouse_x, mouse_y, hit_target.get_center(), True)
            self.spawn_target(0, force_spawn=True)
        else:
            self.score += SCORE_MISS
            self.misses += 1
            self.lives -= 1
            
            # 未命中特效
            self.particle_system.emit_explosion(mouse_x, mouse_y, (255, 80, 80), count=20)
            
            # 寻找最近靶子
            import math
            nearest_target = None
            if self.targets:
                nearest_target = min(self.targets, key=lambda t: math.hypot(t.x - mouse_x, t.y - mouse_y))
            
            target_center = nearest_target.get_center() if nearest_target else (0, 0)
            self.data_tracker.record_click(mouse_x, mouse_y, target_center, False)
            
            if self.lives <= 0:
                self.end_game()
    
    def spawn_target(self, delta_time, force_spawn=False):
        """生成目标（防重叠）"""
        if self.state != GameState.PLAYING:
            return
        
        if len(self.targets) >= MAX_TARGETS:
            return
        
        if force_spawn or len(self.targets) < MAX_TARGETS:
            target_type = random.random()
            
            # 防重叠生成逻辑
            max_attempts = 10
            for attempt in range(max_attempts):
                if target_type < 0.7:
                    radius = random.randint(TARGET_RADIUS_MIN, TARGET_RADIUS_MAX)
                    x = random.randint(radius, SCREEN_WIDTH - radius)
                    y = random.randint(radius, SCREEN_HEIGHT - radius)
                    color = self.target_colors['normal']
                    target = Target(x, y, radius, color)
                
                elif target_type < 0.9:
                    radius = random.randint(max(20, TARGET_RADIUS_MIN - 5), max(35, TARGET_RADIUS_MAX - 10))
                    x = random.randint(radius, SCREEN_WIDTH - radius)
                    y = random.randint(radius, SCREEN_HEIGHT - radius)
                    color = self.target_colors['flick']
                    target = FlickTarget(x, y, radius, color)
                
                else:
                    radius = random.randint(TARGET_RADIUS_MIN + 5, TARGET_RADIUS_MAX)
                    x = random.randint(radius, SCREEN_WIDTH - radius)
                    y = random.randint(radius, SCREEN_HEIGHT - radius)
                    color = self.target_colors['tracking']
                    target = TrackingTarget(x, y, radius, color)
                
                # 检查重叠
                overlap = False
                for existing_target in self.targets:
                    distance = ((target.x - existing_target.x) ** 2 + (target.y - existing_target.y) ** 2) ** 0.5
                    if distance < (target.radius + existing_target.radius + 10):
                        overlap = True
                        break
                
                if not overlap:
                    self.targets.append(target)
                    break
    
    def update(self, delta_time):
        """更新游戏状态"""
        if self.state != GameState.PLAYING:
            return
        
        # 清理死亡靶子
        self.targets = [t for t in self.targets if t.is_alive]
        
        # 生成新靶子
        if len(self.targets) < MAX_TARGETS:
            self.spawn_target(delta_time)
        
        # 更新 Hit Marker
        self.hit_markers = [hm for hm in self.hit_markers if hm.update()]
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # 鼠标点击事件（只在游戏进行中有效）
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.state == GameState.PLAYING:
                    self.handle_click()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC 键行为：菜单/游戏结束时退出，游戏中返回菜单
                    if self.state == GameState.PLAYING:
                        self.state = GameState.MENU
                    else:
                        self.running = False
                
                if event.key == pygame.K_c:
                    self.crosshair.next_style()
                
                # 地图切换（只在菜单界面有效）
                if self.state == GameState.MENU:
                    if event.key == pygame.K_LEFT:
                        self.prev_map()
                    if event.key == pygame.K_RIGHT:
                        self.next_map()
                
                if self.state == GameState.MENU and event.key == pygame.K_SPACE:
                    self.start_game()
                
                if self.state == GameState.GAME_OVER and event.key == pygame.K_SPACE:
                    self.state = GameState.MENU
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.crosshair.update(mouse_x, mouse_y)
    
    def start_game(self):
        """开始游戏"""
        self.state = GameState.PLAYING
        self.score = 0
        self.lives = INITIAL_LIVES
        self.hits = 0
        self.misses = 0
        self.combo = 0
        self.max_combo = 0
        self.targets = []
        self.hit_markers = []
        self.floating_texts = []
        self.particle_system.clear()
        
        self.data_tracker.start_session()
        self.game_start_time = pygame.time.get_ticks()
        
        # 预生成靶子
        for _ in range(MAX_TARGETS):
            self.spawn_target(0)
    
    def end_game(self):
        """结束游戏"""
        self.state = GameState.GAME_OVER
        
        # 数据分析
        self.analyzer = DataAnalyzer(self.data_tracker)
        self.analyzer.process_data()
        
        # 生成报告
        self.visualizer = DataVisualizer(self.analyzer)
        self.visualizer.create_heatmap()
        self.visualizer.create_reaction_time_plot()
        self.visualizer.create_accuracy_pie()
        
        self.report_generator = ReportGenerator(self.analyzer, self.visualizer)
        self.report_filepath = self.report_generator.create_report()
        
        # 计算评级
        self.calculate_cs2_rank()
    
    def calculate_cs2_rank(self):
        """计算 CS2 风格评级"""
        elapsed = (pygame.time.get_ticks() - self.game_start_time) / 1000.0
        accuracy = self.analyzer.metrics['accuracy']
        
        if elapsed == 0:
            elapsed = 0.001
        
        time_score = 10000 / elapsed
        accuracy_score = accuracy * 100
        combo_bonus = self.max_combo * 10
        
        total_score = time_score + accuracy_score + combo_bonus
        
        if total_score >= 15000:
            self.rank = 'S+'
        elif total_score >= 12000:
            self.rank = 'S'
        elif total_score >= 9000:
            self.rank = 'A+'
        elif total_score >= 7000:
            self.rank = 'A'
        elif total_score >= 5000:
            self.rank = 'B+'
        elif total_score >= 3500:
            self.rank = 'B'
        elif total_score >= 2000:
            self.rank = 'C+'
        elif total_score >= 1000:
            self.rank = 'C'
        elif total_score >= 500:
            self.rank = 'D'
        else:
            self.rank = 'F'
        
        self.rank_data = {
            'time_score': time_score,
            'accuracy_score': accuracy_score,
            'combo_bonus': combo_bonus,
            'total_score': total_score,
        }
    
    def draw(self):
        """绘制当前界面"""
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
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
        
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(delta_time)
            self.draw()
        
        pygame.quit()


# HitMarker 类（复用之前的）
class HitMarker:
    """Hit Marker 效果类"""
    
    def __init__(self, x, y, is_headshot=False):
        self.x = x
        self.y = y
        self.is_headshot = is_headshot
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 200
        self.size = 10 if is_headshot else 8
    
    def update(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.spawn_time < self.duration
    
    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.spawn_time
        alpha = max(0, 255 - int((elapsed / self.duration) * 255))
        
        hit_marker_surface = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
        color = (255, 255, 255, alpha)
        line_width = 2
        
        pygame.draw.line(hit_marker_surface, color, (self.size, self.size), 
                        (self.size * 2, self.size * 2), line_width)
        pygame.draw.line(hit_marker_surface, color, 
                        (self.size * 2, self.size), (self.size, self.size * 2), line_width)
        
        if self.is_headshot:
            pygame.draw.circle(hit_marker_surface, (255, 215, 0, alpha), 
                             (int(self.size * 1.5), int(self.size * 1.5)), self.size // 2, 1)
        
        screen.blit(hit_marker_surface, (self.x - self.size, self.y - self.size), 
                   special_flags=pygame.BLEND_RGBA_ADD)
