"""
DataAnalyzer 类 - 组员 A 负责
使用 Pandas 进行数据清洗和分析
计算 TTK、偏移率等关键指标
作者学号：请在此处填写你的学号
"""
import pandas as pd
import numpy as np
from data_tracker import DataTracker


class DataAnalyzer:
    """数据分析器类"""
    
    def __init__(self, data_tracker):
        """
        初始化数据分析器
        
        参数:
            data_tracker: DataTracker 实例
        """
        self.data_tracker = data_tracker
        self.df = None
        self.metrics = {}
    
    def process_data(self):
        """
        将 DataTracker 数据转换为 DataFrame 并计算指标
        """
        clicks = self.data_tracker.get_clicks()
        
        if not clicks:
            self.df = pd.DataFrame()
            self.metrics = {
                'total_clicks': 0,
                'hits': 0,
                'misses': 0,
                'accuracy': 0.0,
                'avg_ttk': 0.0,
                'avg_offset': 0.0
            }
            return
        
        self.df = pd.DataFrame(clicks)
        
        self.metrics['total_clicks'] = len(self.df)
        self.metrics['hits'] = len(self.df[self.df['hit'] == True])
        self.metrics['misses'] = len(self.df[self.df['hit'] == False])
        
        total = self.metrics['hits'] + self.metrics['misses']
        self.metrics['accuracy'] = (self.metrics['hits'] / total * 100) if total > 0 else 0.0
        
        self.metrics['avg_ttk'] = self.calculate_avg_ttk()
        
        self.metrics['avg_offset'] = self.calculate_avg_offset()
    
    def calculate_avg_ttk(self):
        """
        计算平均击杀时间 (TTK - Time To Kill)
        
        返回:
            float: 平均 TTK（毫秒）
        """
        if self.df is None or self.df.empty:
            return 0.0
        
        hits_df = self.df[self.df['hit'] == True]
        
        if hits_df.empty:
            return 0.0
        
        hit_times = hits_df['timestamp'].tolist()
        
        if len(hit_times) < 2:
            return 0.0
        
        ttk_values = []
        for i in range(1, len(hit_times)):
            ttk = hit_times[i] - hit_times[i-1]
            ttk_values.append(ttk)
        
        avg_ttk = np.mean(ttk_values) * 1000
        
        return avg_ttk
    
    def calculate_avg_offset(self):
        """
        计算平均偏移率（未命中点击距离靶心的平均距离）
        
        返回:
            float: 平均偏移距离（像素）
        """
        if self.df is None or self.df.empty:
            return 0.0
        
        misses_df = self.df[self.df['hit'] == False]
        
        if misses_df.empty:
            return 0.0
        
        # 【修复】计算鼠标点击坐标与最近目标坐标的直线距离
        dx = misses_df['mouse_x'] - misses_df['target_x']
        dy = misses_df['mouse_y'] - misses_df['target_y']
        offsets = np.sqrt(dx**2 + dy**2)
        
        return np.mean(offsets)
    
    def get_reaction_times(self):
        """
        获取每次击杀的反应时间序列
        
        返回:
            list: 反应时间列表（毫秒）
        """
        if self.df is None or self.df.empty:
            return []
        
        hits_df = self.df[self.df['hit'] == True]
        hit_times = hits_df['timestamp'].tolist()
        
        if len(hit_times) < 2:
            return []
        
        reaction_times = []
        for i in range(1, len(hit_times)):
            rt = (hit_times[i] - hit_times[i-1]) * 1000
            reaction_times.append(rt)
        
        return reaction_times
    
    def get_metrics(self):
        """
        获取所有计算后的指标
        
        返回:
            dict: 指标字典
        """
        return self.metrics
    
    def export_to_csv(self, filepath):
        """
        导出数据到 CSV 文件
        
        参数:
            filepath: 文件路径
        """
        if self.df is not None and not self.df.empty:
            self.df.to_csv(filepath, index=False, encoding='utf-8-sig')
