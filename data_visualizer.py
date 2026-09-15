"""
DataVisualizer 类 - 组员 B 负责
使用 Matplotlib 绘制热力图和反应时间折线图
作者学号：请在此处填写你的学号
"""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
from config import SCREEN_WIDTH, SCREEN_HEIGHT, REPORTS_DIR


class DataVisualizer:
    """数据可视化器类"""
    
    def __init__(self, analyzer):
        """
        初始化可视化器
        
        参数:
            analyzer: DataAnalyzer 实例
        """
        self.analyzer = analyzer
        self.plots = {}
    
    def create_heatmap(self, filename='heatmap.png'):
        """
        绘制火力分布热力图
        
        显示所有未命中点击的分布情况
        
        参数:
            filename: 保存的文件名
            
        返回:
            str: 文件完整路径
        """
        df = self.analyzer.df
        
        if df is None or df.empty:
            return None
        
        misses_df = df[df['hit'] == False]
        
        if misses_df.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'No misses recorded', ha='center', va='center', fontsize=16)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            filepath = f"{REPORTS_DIR}/{filename}"
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            return filepath
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        scatter = ax.scatter(
            misses_df['mouse_x'],
            misses_df['mouse_y'],
            c=misses_df['timestamp'],
            cmap='Reds',
            alpha=0.6,
            s=50,
            edgecolors='black',
            linewidth=0.5
        )
        
        ax.set_xlim(0, SCREEN_WIDTH)
        ax.set_ylim(SCREEN_HEIGHT, 0)
        ax.set_xlabel('X Position (pixels)', fontsize=12)
        ax.set_ylabel('Y Position (pixels)', fontsize=12)
        ax.set_title('Miss Distribution Heatmap\n火力分布热力图', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        cbar = plt.colorbar(scatter)
        cbar.set_label('Time (seconds)', fontsize=10)
        
        filepath = f"{REPORTS_DIR}/{filename}"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        self.plots['heatmap'] = filepath
        return filepath
    
    def create_reaction_time_plot(self, filename='reaction_time.png'):
        """
        绘制反应时间折线图
        
        展示 TTK 随时间的变化
        
        参数:
            filename: 保存的文件名
            
        返回:
            str: 文件完整路径
        """
        reaction_times = self.analyzer.get_reaction_times()
        
        if not reaction_times:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=16)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            filepath = f"{REPORTS_DIR}/{filename}"
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            return filepath
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = range(1, len(reaction_times) + 1)
        ax.plot(x, reaction_times, marker='o', linestyle='-', linewidth=2, 
               markersize=6, color='blue', alpha=0.7)
        
        if reaction_times:
            avg_rt = np.mean(reaction_times)
            ax.axhline(y=avg_rt, color='red', linestyle='--', linewidth=2, 
                      label=f'Average: {avg_rt:.1f}ms')
            ax.legend(loc='upper right')
        
        ax.set_xlabel('Kill Sequence', fontsize=12)
        ax.set_ylabel('Time To Kill (ms)', fontsize=12)
        ax.set_title('Reaction Time Analysis\n反应时间折线图', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(bottom=0)
        
        filepath = f"{REPORTS_DIR}/{filename}"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        self.plots['reaction_time'] = filepath
        return filepath
    
    def create_accuracy_pie(self, filename='accuracy_pie.png'):
        """
        绘制命中率饼图
        
        参数:
            filename: 保存的文件名
            
        返回:
            str: 文件完整路径
        """
        metrics = self.analyzer.get_metrics()
        
        hits = metrics.get('hits', 0)
        misses = metrics.get('misses', 0)
        
        if hits + misses == 0:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=16)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            filepath = f"{REPORTS_DIR}/{filename}"
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            return filepath
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        sizes = [hits, misses]
        labels = [f'Hits: {hits}', f'Misses: {misses}']
        colors = ['#2ecc71', '#e74c3c']
        explode = (0.05, 0)
        
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
              startangle=90, shadow=True)
        ax.set_title('Accuracy Statistics\n命中率统计', fontsize=14, fontweight='bold')
        
        filepath = f"{REPORTS_DIR}/{filename}"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        self.plots['accuracy_pie'] = filepath
        return filepath
    
    def get_all_plots(self):
        """获取所有生成的图表路径"""
        return self.plots
