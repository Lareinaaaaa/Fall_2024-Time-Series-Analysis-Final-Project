"""
Created by Jiajun Chen and Xinyue on Dec 8 2024
"""

from graphviz import Digraph
from PIL import Image
import os


desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')


dot = Digraph()


dot.attr(rankdir='TB', bgcolor='#FFFFFF')

# 设置边的默认样式，颜色为黑色
dot.attr('edge', color='#000000', arrowsize='1.0')

# 定义节点
dot.node('Start', 'Start', shape='rect', style='rounded, filled', fillcolor='#f2f4c0')  # 黄色
dot.node('ComputeGamma', 'Compute γ', shape='ellipse', style='filled', fillcolor='#ffe1bb')  # 橙色
dot.node('Init', 'Initialize δ, δ̂', shape='ellipse', style='filled', fillcolor='#cde6d1')  # 绿色
dot.node('IterativeLoop', 'Iterative Loop', shape='rect', style='rounded, filled', fillcolor='#fddee3')  # 红色
dot.node('SolveU', 'Solve for u', shape='ellipse', style='filled', fillcolor='#ffe1bb')  # 橙色
dot.node('ComputeA', 'Compute a', shape='ellipse', style='filled', fillcolor='#ffe1bb')  # 橙色
dot.node('UpdateDelta', 'Update δ', shape='ellipse', style='filled', fillcolor='#c4e7fa')  # 蓝色
dot.node('CheckConverged', 'Converged?', shape='rect', style='rounded, filled', fillcolor='#fddee3')  # 红色
dot.node('End', 'End', shape='rect', style='rounded, filled', fillcolor='#f2f4c0')  # 黄色

# 添加边
dot.edge('Start', 'ComputeGamma')
dot.edge('ComputeGamma', 'Init')
dot.edge('Init', 'IterativeLoop')
dot.edge('IterativeLoop', 'SolveU')
dot.edge('IterativeLoop', 'ComputeA')
dot.edge('SolveU', 'UpdateDelta')
dot.edge('ComputeA', 'UpdateDelta')
dot.edge('UpdateDelta', 'CheckConverged')
dot.edge('CheckConverged', 'IterativeLoop', label='No')
dot.edge('CheckConverged', 'End', label='Yes')

# 使用子图分组节点以更均匀分布
with dot.subgraph() as sub:
    sub.attr(rank='same')  # 将 IterativeLoop, SolveU 和 ComputeA 放在同一层
    sub.node('IterativeLoop')
    sub.node('SolveU')
    sub.node('ComputeA')

# 保存图像到桌面
output_path = os.path.join(desktop_path, 'mean_field_algorithm_square')
dot.render(output_path, format='png', cleanup=True)

# 打开生成的 PNG 图像
img = Image.open(output_path + '.png')
img.show()
