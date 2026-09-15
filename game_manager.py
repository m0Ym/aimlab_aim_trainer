"""
GameManager 类 - 组员 A 负责
游戏核心管理器，控制游戏状态和流程
作者学号：请在此处填写你的学号
"""
import pygame
import random
from enum import Enum
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, INITIAL_LIVES, GAME_DURATION
from config import TARGET_SPAWN_RATE, SCORE_HIT, SCORE_MISS, MAX_TARGETS
from config import TARGET_RADIUS_MIN, TARGET_RADIUS_MAX
from config import BG_COLOR, GRID_COLOR, UI_TEXT_COLOR, UI_PANEL_BG, UI_ACCENT_COLOR
from config import TARGET_COLORS
from target import Target
from crosshair import Crosshair
from target_types import FlickTarget, TrackingTarget, HeadshotTarget
from data_tracker import DataTracker
from data_analyzer import DataAnalyzer
from data_visualizer import DataVisualizer
from report_generator import ReportGenerator


class GameState(Enum):
    """游戏状态枚举"""
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3


class HitMarker:
    """Hit Marker 效果类（命中提示）"""
    
    def __init__(self, x, y, is_headshot=False):
        """
        初始化 Hit Marker
        
        参数:
            x: X 坐标
            y: Y 坐标
            is_headshot: 是否爆头
        """
        self.x = x
        self.y = y
        self.is_headshot = is_headshot
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 200  # 持续 200ms
        self.size = 10 if is_headshot else 8
    
    def update(self):
        """更新状态"""
        current_time = pygame.time.get_ticks()
        return current_time - self.spawn_time < self.duration
    
    def draw(self, screen):
        """绘制 Hit Marker"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.spawn_time
        
        # 计算透明度（逐渐消失）
        alpha = max(0, 255 - int((elapsed / self.duration) * 255))
        
        # 创建支持透明度的 Surface
        hit_marker_surface = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
        
        # 绘制 X 形状
        color = (255, 255, 255, alpha)  # 白色
        line_width = 2
        
        # 第一条线
        pygame.draw.line(hit_marker_surface, color, 
                        (self.size, self.size), 
                        (self.size * 2, self.size * 2), 
                        line_width)
        # 第二条线
        pygame.draw.line(hit_marker_surface, color, 
                        (self.size * 2, self.size), 
                        (self.size, self.size * 2), 
                        line_width)
        
        # 爆头额外绘制一个圆圈
        if self.is_headshot:
            pygame.draw.circle(hit_marker_surface, (255, 215, 0, alpha), 
                             (int(self.size * 1.5), int(self.size * 1.5)), 
                             self.size // 2, 1)
        
        screen.blit(hit_marker_surface, (self.x - self.size, self.y - self.size), special_flags=pygame.BLEND_RGBA_ADD)


class GameManager:
    """游戏管理器类"""
    
    def __init__(self):
        """初始化游戏管理器（窗口模式）"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Aim Lab 练枪模拟器 - 窗口模式 (可拖动调整大小)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        
        self.state = GameState.MENU
        self.crosshair = Crosshair()
        self.targets = []
        self.score = 0
        self.lives = INITIAL_LIVES
        self.game_start_time = 0
        self.spawn_timer = 0
        self.hits = 0
        self.misses = 0
        
        self.data_tracker = DataTracker()
        self.rank = None
        self.rank_data = {}
        
        self.hit_markers = []  # Hit Marker 列表
        
        self.running = True
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_click()
            
            if event.type == pygame.KEYDOWN:
                # 调试：打印所有按键
                print(f"检测到按键：{event.key}")
                
                if event.key == pygame.K_ESCAPE:
                    print("按下了 ESC 键")
                    self.running = False
                
                if event.key == pygame.K_c:  # 按 C 键切换准星（任何状态都可以）
                    print(f"按下了 C 键，准备切换准星")
                    self.crosshair.next_style()
                    print(f"切换到准星：{self.crosshair.get_style_name()}")
                
                if self.state == GameState.MENU and event.key == pygame.K_SPACE:
                    print("按下了 SPACE 键，开始游戏")
                    self.start_game()
                
                if self.state == GameState.GAME_OVER and event.key == pygame.K_SPACE:
                    print("按下了 SPACE 键，返回菜单")
                    self.state = GameState.MENU
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.crosshair.update(mouse_x, mouse_y)
    
    def handle_click(self):
        """处理鼠标点击（CS2 模式：击破后立即生成，带 Hit Marker）"""
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
                
                # 添加 Hit Marker 效果
                is_headshot = hasattr(target, 'is_headshot') and target.is_headshot
                self.hit_markers.append(HitMarker(mouse_x, mouse_y, is_headshot))
                
                target.destroy()
                break
        
        if hit:
            self.data_tracker.record_click(mouse_x, mouse_y, hit_target.get_center(), True)
            self.spawn_target(0, force_spawn=True)
        else:
            self.score += SCORE_MISS
            self.misses += 1
            self.lives -= 1
            
            # 【修复】寻找距离鼠标最近的靶子计算误差
            import math
            nearest_target = None
            if self.targets:
                nearest_target = min(self.targets, key=lambda t: math.hypot(t.x - mouse_x, t.y - mouse_y))
            
            target_center = nearest_target.get_center() if nearest_target else (0, 0)
            self.data_tracker.record_click(mouse_x, mouse_y, target_center, False)
            
            if self.lives <= 0:
                self.end_game()
    
    def start_game(self):
        """开始游戏（CS2 模式：预生成 4 个靶子）"""
        self.state = GameState.PLAYING
        self.score = 0
        self.lives = INITIAL_LIVES
        self.game_start_time = pygame.time.get_ticks()
        self.targets = []
        self.hits = 0
        self.misses = 0
        
        self.data_tracker.start_session()
        
        for i in range(MAX_TARGETS):
            self.spawn_target(0)
        
        pygame.mouse.set_visible(False)
    
    def end_game(self):
        """结束游戏并生成报告（CS2 评级系统）"""
        self.state = GameState.GAME_OVER
        pygame.mouse.set_visible(True)
        
        self.analyzer = DataAnalyzer(self.data_tracker)
        self.analyzer.process_data()
        
        self.visualizer = DataVisualizer(self.analyzer)
        self.visualizer.create_heatmap()
        self.visualizer.create_reaction_time_plot()
        self.visualizer.create_accuracy_pie()
        
        self.report_generator = ReportGenerator(self.analyzer, self.visualizer)
        self.report_filepath = self.report_generator.create_report()
        
        self.calculate_cs2_rank()
        
        print(f"\n游戏结束！")
        print(f"最终得分：{self.score}")
        print(f"命中率：{self.analyzer.metrics['accuracy']:.1f}%")
        print(f"平均 TTK: {self.analyzer.metrics['avg_ttk']:.1f}ms")
        print(f"评级：{self.rank}")
        print(f"报告已生成：{self.report_filepath}")
    
    def spawn_target(self, delta_time, force_spawn=False):
        """
        生成目标（CS2 模式：同屏最多 4 个，击破后立即生成，防重叠）
        
        参数:
            delta_time: 时间间隔
            force_spawn: 是否强制生成（击破后立即生成）
        """
        if self.state != GameState.PLAYING:
            return
        
        if len(self.targets) >= MAX_TARGETS:
            return
        
        if force_spawn or len(self.targets) < MAX_TARGETS:
            target_type = random.random()
            
            # 【新增】防重叠生成逻辑
            max_attempts = 10  # 最多尝试 10 次
            for attempt in range(max_attempts):
                if target_type < 0.7:
                    # 普通靶 - 极光蓝
                    radius = random.randint(TARGET_RADIUS_MIN, TARGET_RADIUS_MAX)
                    x = random.randint(radius, SCREEN_WIDTH - radius)
                    y = random.randint(radius, SCREEN_HEIGHT - radius)
                    color = TARGET_COLORS['normal']
                    target = Target(x, y, radius, color)
                
                elif target_type < 0.9:
                    # 闪现靶 - 霓虹粉
                    radius = random.randint(max(20, TARGET_RADIUS_MIN - 5), max(35, TARGET_RADIUS_MAX - 10))
                    x = random.randint(radius, SCREEN_WIDTH - radius)
                    y = random.randint(radius, SCREEN_HEIGHT - radius)
                    color = TARGET_COLORS['flick']
                    target = FlickTarget(x, y, radius, color)
                
                else:
                    # 追踪靶 - 电竞黄
                    radius = random.randint(TARGET_RADIUS_MIN + 5, TARGET_RADIUS_MAX)
                    x = random.randint(radius, SCREEN_WIDTH - radius)
                    y = random.randint(radius, SCREEN_HEIGHT - radius)
                    color = TARGET_COLORS['tracking']
                    target = TrackingTarget(x, y, radius, color)
                
                # 检查是否与现有靶子重叠
                overlap = False
                for existing_target in self.targets:
                    distance = ((target.x - existing_target.x) ** 2 + (target.y - existing_target.y) ** 2) ** 0.5
                    if distance < (target.radius + existing_target.radius + 10):  # 留 10 像素间隙
                        overlap = True
                        break
                
                if not overlap:
                    self.targets.append(target)
                    break
    
    def update(self, delta_time):
        """更新游戏状态（CS2 模式）"""
        if self.state == GameState.PLAYING:
            elapsed_time = (pygame.time.get_ticks() - self.game_start_time) / 1000.0
            
            if elapsed_time >= GAME_DURATION:
                self.end_game()
            
            # 清理已死亡的靶子
            self.targets = [t for t in self.targets if t.is_alive]
            
            # 如果靶子数量不足，生成新靶子
            if len(self.targets) < MAX_TARGETS:
                self.spawn_target(delta_time)
        
        # 更新 Hit Marker
        self.hit_markers = [hm for hm in self.hit_markers if hm.update()]
    
    def draw_background(self):
        """绘制电竞风格的网格背景"""
        self.screen.fill(BG_COLOR)
        grid_size = 80  # 网格大小
        
        # 绘制垂直线
        for x in range(0, SCREEN_WIDTH, grid_size):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT), 1)
        
        # 绘制水平线
        for y in range(0, SCREEN_HEIGHT, grid_size):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)
        
        # 中心十字暗线，增强聚焦感
        pygame.draw.line(self.screen, (50, 55, 60), (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT), 2)
        pygame.draw.line(self.screen, (50, 55, 60), (0, SCREEN_HEIGHT//2), (SCREEN_WIDTH, SCREEN_HEIGHT//2), 2)
    
    def draw_menu(self):
        """绘制主菜单（显示准星设置）"""
        self.draw_background()
        
        # 半透明面板
        panel = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        panel.fill((15, 18, 20, 200))
        self.screen.blit(panel, (0, 0))
        
        title = self.font.render("Aim Lab 练枪模拟器", True, UI_ACCENT_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title, title_rect)
        
        start_text = self.small_font.render("按 SPACE 开始游戏", True, (0, 255, 0))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(start_text, start_rect)
        
        crosshair_info = self.small_font.render(f"当前准星：{self.crosshair.get_style_name()}", True, UI_ACCENT_COLOR)
        crosshair_rect = crosshair_info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(crosshair_info, crosshair_rect)
        
        switch_text = self.small_font.render("按 C 键切换准星风格", True, (255, 255, 0))
        switch_rect = switch_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
        self.screen.blit(switch_text, switch_rect)
        
        quit_text = self.small_font.render("按 ESC 退出", True, (255, 0, 0))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140))
        self.screen.blit(quit_text, quit_rect)
    
    def draw_game(self):
        """绘制游戏界面（CS2 风格）"""
        self.draw_background()
        
        for target in self.targets:
            target.draw(self.screen)
        
        # 绘制 Hit Marker
        for hit_marker in self.hit_markers:
            hit_marker.draw(self.screen)
        
        self.crosshair.draw(self.screen)
        
        # 顶部数据面板
        self.draw_ui_panel()
        
        elapsed = (pygame.time.get_ticks() - self.game_start_time) / 1000.0
        time_text = self.small_font.render(f"Time: {elapsed:.2f}s", True, UI_TEXT_COLOR)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH - 150, 25))
        self.screen.blit(time_text, time_rect)
    
    def draw_ui_panel(self):
        """绘制顶部数据面板（磨砂玻璃效果）"""
        # 创建一个支持透明度的 Surface
        panel = pygame.Surface((SCREEN_WIDTH, 50), pygame.SRCALPHA)
        panel.fill(UI_PANEL_BG)
        self.screen.blit(panel, (0, 0))
        
        # 在这个面板上渲染文本
        score_text = self.small_font.render(f"Score: {self.score}", True, UI_ACCENT_COLOR)
        score_rect = score_text.get_rect(left=20, centery=25)
        self.screen.blit(score_text, score_rect)
        
        lives_text = self.small_font.render(f"Lives: {self.lives}", True, (255, 100, 100))
        lives_rect = lives_text.get_rect(left=200, centery=25)
        self.screen.blit(lives_text, lives_rect)
        
        targets_text = self.small_font.render(f"Targets: {len(self.targets)}/{MAX_TARGETS}", True, (255, 255, 100))
        targets_rect = targets_text.get_rect(left=380, centery=25)
        self.screen.blit(targets_text, targets_rect)
    
    def draw_game_over(self):
        """绘制游戏结束界面（CS2 评级风格）"""
        self.screen.fill((30, 30, 30))
        
        rank_colors = {
            'S+': (255, 215, 0),
            'S': (255, 215, 0),
            'A+': (191, 64, 191),
            'A': (191, 64, 191),
            'B+': (0, 191, 255),
            'B': (0, 191, 255),
            'C+': (255, 165, 0),
            'C': (255, 165, 0),
            'D': (255, 69, 0),
            'F': (128, 128, 128)
        }
        
        if hasattr(self, 'rank') and self.rank:
            rank_color = rank_colors.get(self.rank, (255, 255, 255))
            
            rank_text = self.font.render(f"Rank: {self.rank}", True, rank_color)
            rank_rect = rank_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            self.screen.blit(rank_text, rank_rect)
        
        game_over_text = self.small_font.render("Session Complete", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(game_over_text, game_over_rect)
        
        final_score = self.small_font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(final_score, score_rect)
        
        if hasattr(self, 'analyzer') and hasattr(self, 'rank_data'):
            accuracy = self.analyzer.metrics['accuracy']
            ttk = self.analyzer.metrics['avg_ttk']
            time_spent = self.rank_data.get('time', 0)
            hits = self.rank_data.get('hits', 0)
            
            stats = [
                f"Time: {time_spent:.2f}s",
                f"Accuracy: {accuracy:.1f}%",
                f"TTK: {ttk:.0f}ms",
                f"Targets: {hits}"
            ]
            
            for i, stat in enumerate(stats):
                y_offset = SCREEN_HEIGHT // 2 + 70 + i * 40
                stat_text = self.small_font.render(stat, True, (200, 200, 200))
                stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                self.screen.blit(stat_text, stat_rect)
            
            restart_text = self.small_font.render("Press SPACE to continue", True, (0, 255, 0))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250))
            self.screen.blit(restart_text, restart_rect)
        else:
            accuracy = (self.hits / (self.hits + self.misses) * 100) if (self.hits + self.misses) > 0 else 0
            acc_text = self.small_font.render(f"Accuracy: {accuracy:.1f}%", True, (255, 255, 255))
            acc_rect = acc_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            self.screen.blit(acc_text, acc_rect)
            
            restart_text = self.small_font.render("Press SPACE to continue", True, (0, 255, 0))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140))
            self.screen.blit(restart_text, restart_rect)
    
    def calculate_cs2_rank(self):
        """
        计算 CS2 风格的评级（基于时间和准确率）
        
        评级标准（参考 CS2 和 Aim Lab）:
        - S+: 时间<30s 且 准确率>90%
        - S: 时间<40s 且 准确率>85%
        - A+: 时间<45s 且 准确率>80%
        - A: 时间<50s 且 准确率>75%
        - B+: 时间<55s 且 准确率>70%
        - B: 时间<60s 且 准确率>65%
        - C+: 时间<65s 且 准确率>60%
        - C: 时间<70s 且 准确率>55%
        - D: 时间>=70s 或 准确率<55%
        """
        metrics = self.analyzer.get_metrics()
        accuracy = metrics['accuracy']
        avg_ttk = metrics['avg_ttk']
        total_hits = metrics['hits']
        
        elapsed = (pygame.time.get_ticks() - self.game_start_time) / 1000.0
        
        self.rank_data = {
            'time': elapsed,
            'accuracy': accuracy,
            'avg_ttk': avg_ttk,
            'hits': total_hits
        }
        
        if total_hits == 0:
            self.rank = 'F'
            return
        
        if elapsed < 30 and accuracy >= 90:
            self.rank = 'S+'
        elif elapsed < 40 and accuracy >= 85:
            self.rank = 'S'
        elif elapsed < 45 and accuracy >= 80:
            self.rank = 'A+'
        elif elapsed < 50 and accuracy >= 75:
            self.rank = 'A'
        elif elapsed < 55 and accuracy >= 70:
            self.rank = 'B+'
        elif elapsed < 60 and accuracy >= 65:
            self.rank = 'B'
        elif elapsed < 65 and accuracy >= 60:
            self.rank = 'C+'
        elif elapsed < 70 and accuracy >= 55:
            self.rank = 'C'
        else:
            self.rank = 'D'
    
    def draw(self):
        """绘制当前帧"""
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(delta_time)
            self.draw()
        
        pygame.quit()


if __name__ == "__main__":
    game = GameManager()
    game.run()
