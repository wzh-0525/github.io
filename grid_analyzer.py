#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询网格分析工具
用于分析领域与意图的交叉分布
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.font_manager as fm
import warnings
import os
import sys

warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class QueryGridAnalyzer:
    def __init__(self, excel_file=None):
        """初始化分析器"""
        self.excel_file = excel_file
        self.data = None
        if excel_file and os.path.exists(excel_file):
            self.load_data()
        else:
            self.create_sample_data()
    
    def load_data(self):
        """加载Excel数据"""
        try:
            self.data = pd.read_excel(self.excel_file)
            print(f"成功加载数据，共 {len(self.data)} 行")
            print(f"列名: {list(self.data.columns)}")
            
            # 显示数据基本信息
            print("\n数据预览:")
            print(self.data.head())
            
            # 检查必要的列
            required_cols = ['First_domain', 'Second_Domain', 'First_Intent', 'Second_Intent']
            missing_cols = [col for col in required_cols if col not in self.data.columns]
            if missing_cols:
                print(f"警告: 缺少列 {missing_cols}")
                
        except Exception as e:
            print(f"加载数据失败: {e}")
            print("使用示例数据...")
            self.create_sample_data()
    
    def create_sample_data(self):
        """创建示例数据"""
        print("创建示例数据...")
        np.random.seed(42)
        
        # 定义领域和意图
        first_domains = ['技术', '生活', '娱乐', '教育', '商业']
        second_domains = {
            '技术': ['人工智能', '机器学习', '数据科学', '云计算', '区块链'],
            '生活': ['健康', '美食', '旅游', '购物', '家居'],
            '娱乐': ['电影', '音乐', '游戏', '体育', '阅读'],
            '教育': ['语言学习', '职业培训', '学术研究', '在线课程', '考试'],
            '商业': ['电商', '金融', '营销', '管理', '创业']
        }
        
        first_intents = ['查询', '学习', '咨询', '推荐', '购买']
        second_intents = {
            '查询': ['定义查询', '应用查询', '比较查询', '价格查询', '位置查询'],
            '学习': ['教程学习', '技能学习', '理论学习', '实践学习', '考试学习'],
            '咨询': ['医疗咨询', '法律咨询', '技术咨询', '投资咨询', '生活咨询'],
            '推荐': ['内容推荐', '产品推荐', '服务推荐', '地点推荐', '人员推荐'],
            '购买': ['在线购买', '比价购买', '团购', '预订', '租赁']
        }
        
        # 生成示例数据
        data_list = []
        for _ in range(2000):
            first_domain = np.random.choice(first_domains)
            second_domain = np.random.choice(second_domains[first_domain])
            first_intent = np.random.choice(first_intents)
            second_intent = np.random.choice(second_intents[first_intent])
            
            data_list.append({
                'First_domain': first_domain,
                'Second_Domain': second_domain,
                'First_Intent': first_intent,
                'Second_Intent': second_intent,
                'query': f'示例查询_{len(data_list) + 1}'
            })
        
        self.data = pd.DataFrame(data_list)
        print(f"创建了 {len(self.data)} 条示例数据")
    
    def create_grid_matrix(self, domain_level='first', intent_level='first'):
        """创建网格矩阵"""
        # 确定使用的列
        domain_col = 'First_domain' if domain_level == 'first' else 'Second_Domain'
        intent_col = 'First_Intent' if intent_level == 'first' else 'Second_Intent'
        
        # 检查列是否存在
        if domain_col not in self.data.columns or intent_col not in self.data.columns:
            print(f"警告: 列 {domain_col} 或 {intent_col} 不存在")
            return None, None, None
        
        # 创建交叉表
        cross_table = pd.crosstab(
            self.data[domain_col], 
            self.data[intent_col], 
            margins=False
        )
        
        return cross_table, domain_col, intent_col
    
    def plot_heatmap(self, domain_level='first', intent_level='first', figsize=(12, 8), save_path=None):
        """绘制热力图"""
        cross_table, domain_col, intent_col = self.create_grid_matrix(domain_level, intent_level)
        
        if cross_table is None:
            return None
        
        # 创建图形
        fig, ax = plt.subplots(figsize=figsize)
        
        # 创建蓝色渐变色彩映射
        colors = ['#f8f9fa', '#e3f2fd', '#bbdefb', '#90caf9', '#64b5f6', 
                 '#42a5f5', '#2196f3', '#1e88e5', '#1976d2', '#1565c0', '#0d47a1']
        n_bins = len(colors)
        cmap = LinearSegmentedColormap.from_list('blue_gradient', colors, N=n_bins)
        
        # 绘制热力图
        sns.heatmap(cross_table, 
                   annot=True, 
                   fmt='d', 
                   cmap=cmap,
                   cbar_kws={'label': '查询数量'},
                   ax=ax,
                   square=False,
                   linewidths=0.5,
                   linecolor='white')
        
        # 设置标题和标签
        domain_level_text = '一级领域' if domain_level == 'first' else '二级领域'
        intent_level_text = '一级意图' if intent_level == 'first' else '二级意图'
        
        ax.set_title(f'查询网格分析 - {domain_level_text} vs {intent_level_text}', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel(f'{intent_level_text}', fontsize=12, fontweight='bold')
        ax.set_ylabel(f'{domain_level_text}', fontsize=12, fontweight='bold')
        
        # 旋转标签以避免重叠
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图片
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"图片已保存到: {save_path}")
        
        return fig
    
    def generate_all_combinations(self, save_dir='output'):
        """生成所有组合的热力图"""
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        combinations = [
            ('first', 'first', '一级领域_vs_一级意图'),
            ('first', 'second', '一级领域_vs_二级意图'),
            ('second', 'first', '二级领域_vs_一级意图'),
            ('second', 'second', '二级领域_vs_二级意图')
        ]
        
        for domain_level, intent_level, filename in combinations:
            print(f"生成 {filename} 热力图...")
            save_path = os.path.join(save_dir, f'{filename}.png')
            fig = self.plot_heatmap(domain_level, intent_level, save_path=save_path)
            if fig:
                plt.close(fig)  # 关闭图形以释放内存
    
    def get_statistics(self, domain_level='first', intent_level='first'):
        """获取统计信息"""
        cross_table, domain_col, intent_col = self.create_grid_matrix(domain_level, intent_level)
        
        if cross_table is None:
            return None
        
        stats = {
            'total_queries': len(self.data),
            'total_domains': len(cross_table.index),
            'total_intents': len(cross_table.columns),
            'max_count': cross_table.max().max(),
            'min_count': cross_table.min().min(),
            'mean_count': cross_table.mean().mean(),
            'std_count': cross_table.std().std()
        }
        
        return stats
    
    def print_statistics(self, domain_level='first', intent_level='first'):
        """打印统计信息"""
        stats = self.get_statistics(domain_level, intent_level)
        
        if stats is None:
            print("无法获取统计信息")
            return
        
        domain_level_text = '一级领域' if domain_level == 'first' else '二级领域'
        intent_level_text = '一级意图' if intent_level == 'first' else '二级意图'
        
        print(f"\n=== {domain_level_text} vs {intent_level_text} 统计信息 ===")
        print(f"总查询数: {stats['total_queries']}")
        print(f"领域数量: {stats['total_domains']}")
        print(f"意图数量: {stats['total_intents']}")
        print(f"最大计数: {stats['max_count']}")
        print(f"最小计数: {stats['min_count']}")
        print(f"平均计数: {stats['mean_count']:.2f}")
        print(f"标准差: {stats['std_count']:.2f}")
    
    def export_matrix_to_csv(self, domain_level='first', intent_level='first', save_path=None):
        """导出矩阵到CSV"""
        cross_table, domain_col, intent_col = self.create_grid_matrix(domain_level, intent_level)
        
        if cross_table is None:
            print("无法创建矩阵")
            return
        
        if save_path is None:
            save_path = f'query_grid_{domain_level}_{intent_level}.csv'
        
        cross_table.to_csv(save_path, encoding='utf-8-sig')
        print(f"矩阵已导出到: {save_path}")

def main():
    """主函数"""
    # 检查是否提供了Excel文件路径
    excel_file = None
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
        if not os.path.exists(excel_file):
            print(f"文件不存在: {excel_file}")
            excel_file = None
    
    # 创建分析器
    analyzer = QueryGridAnalyzer(excel_file)
    
    # 打印所有组合的统计信息
    combinations = [
        ('first', 'first'),
        ('first', 'second'),
        ('second', 'first'),
        ('second', 'second')
    ]
    
    for domain_level, intent_level in combinations:
        analyzer.print_statistics(domain_level, intent_level)
    
    # 生成所有热力图
    print("\n开始生成热力图...")
    analyzer.generate_all_combinations()
    
    # 导出CSV文件
    print("\n导出CSV文件...")
    for domain_level, intent_level in combinations:
        analyzer.export_matrix_to_csv(domain_level, intent_level)
    
    print("\n分析完成！")
    print("生成的文件:")
    print("- output/一级领域_vs_一级意图.png")
    print("- output/一级领域_vs_二级意图.png") 
    print("- output/二级领域_vs_一级意图.png")
    print("- output/二级领域_vs_二级意图.png")
    print("- query_grid_first_first.csv")
    print("- query_grid_first_second.csv")
    print("- query_grid_second_first.csv")
    print("- query_grid_second_second.csv")

if __name__ == "__main__":
    main()
