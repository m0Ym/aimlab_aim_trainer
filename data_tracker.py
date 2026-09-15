"""
DataTracker 类 - 组员 C 负责
数据追踪器，记录游戏过程中的所有点击数据
作者学号：请在此处填写你的学号
"""
import time
from datetime import datetime


class DataTracker:
    """数据追踪器类"""
    
    def __init__(self):
        """初始化数据追踪器"""
        self.clicks = []
        self.session_id = None
        self.start_time = None
    
    def start_session(self):
        """开始新的游戏会话"""
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = time.perf_counter()
        self.clicks = []
    
    def record_click(self, mouse_x, mouse_y, target_center=None, hit=False):
        """
        记录一次点击
        
        参数:
            mouse_x: 鼠标点击的 X 坐标
            mouse_y: 鼠标点击的 Y 坐标
            target_center: 目标中心坐标 (x, y)，如果未击中则为 None
            hit: 是否击中目标
        """
        click_data = {
            'timestamp': time.perf_counter() - self.start_time if self.start_time else 0,
            'mouse_x': mouse_x,
            'mouse_y': mouse_y,
            'target_x': target_center[0] if target_center else None,
            'target_y': target_center[1] if target_center else None,
            'hit': hit,
            'session_id': self.session_id
        }
        self.clicks.append(click_data)
    
    def get_clicks(self):
        """获取所有点击记录"""
        return self.clicks
    
    def get_hits(self):
        """获取所有击中的点击"""
        return [c for c in self.clicks if c['hit']]
    
    def get_misses(self):
        """获取所有未击中的点击"""
        return [c for c in self.clicks if not c['hit']]
    
    def get_session_duration(self):
        """获取会话时长（秒）"""
        if not self.start_time:
            return 0
        return time.perf_counter() - self.start_time
    
    def export_to_dict(self):
        """导出为字典格式"""
        return {
            'session_id': self.session_id,
            'start_time': self.start_time,
            'total_clicks': len(self.clicks),
            'hits': len(self.get_hits()),
            'misses': len(self.get_misses()),
            'duration': self.get_session_duration(),
            'clicks': self.clicks
        }
    
    def clear(self):
        """清空数据"""
        self.clicks = []
        self.session_id = None
        self.start_time = None
