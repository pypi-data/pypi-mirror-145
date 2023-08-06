# -*- coding: utf-8 -*-
# file: rq3.py
# time: 08/02/2022
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import os

from metric_visualizer import MetricVisualizer

# laptop14_metrics = {
#     'EDA': {
#         'Acc':[84.80,85.42,84.64,85.42,84.17],
#         'F1.pdf':[82.16,82.04,81.69,82.98,81.25],
#     },
#     'SplitAug': {
#         'Acc': [83.54,84.64,83.86,84.17,83.70],
#         'F1.pdf': [80.37,81.58,81.45,80.89,80.83],
#     },
#     'BackTransAug': {
#         'Acc': [82.92,81.97,83.54,82.45,82.76],
#         'F1.pdf': [79.32,78.58,80.07,79.14,79.42],
#     },
#     'SpellingAug': {
#         'Acc': [85.27,85.27,85.11,84.95,84.95],
#         'F1.pdf': [82.49,82.59,82.16,82.07,82.19],
#     },
#     'WordEmbsAug': {
#         'Acc': [84.17,84.80,84.95,85.11,84.48],
#         'F1.pdf': [81.05,81.50,82.06,82.12,81.83],
#     }
# }

laptop14_metrics = {
    'Acc': {
        'BackTransAug': [82.92, 81.97, 83.54, 82.45, 82.76],
        'EDA': [84.80, 85.42, 84.64, 85.42, 84.17],
        'SplitAug': [83.54, 84.64, 83.86, 84.17, 83.70],
        'SpellingAug': [85.27, 85.27, 85.11, 84.95, 84.95],
        'WordEmbsAug': [84.17, 84.80, 84.95, 85.11, 84.48]
    },
    'F1.pdf': {
        'BackTransAug': [79.32, 78.58, 80.07, 79.14, 79.42],
        'EDA': [82.16, 82.04, 81.69, 82.98, 81.25],
        'SplitAug': [80.37, 81.58, 81.45, 80.89, 80.83],
        'SpellingAug': [82.49, 82.59, 82.16, 82.07, 82.19],
        'WordEmbsAug': [81.05, 81.50, 82.06, 82.12, 81.83]
    }
}
rest14_metrics = {

}
MV = MetricVisualizer(laptop14_metrics)
MV.violin_plot(xlabel='Base Augment Method', xtickshift=5, xrotation=30, xticks=['BackTrans', 'EDA', 'SplitAug', 'SpellingAug', 'WordEmbs'])
MV.box_plot(xlabel='Base Augment Method', xrotation=30, xticks=['BackTrans', 'EDA', 'SplitAug', 'SpellingAug', 'WordEmbs'])

MV.violin_plot(save_path='Laptop14', xlabel='', xtickshift=5, xrotation=30, yticks='Metrics', xticks=['BackTrans', 'EDA', 'SplitAug', 'SpellingAug', 'WordEmbs'])
MV.box_plot(save_path='Laptop14', xlabel='', widths=0.7, xtickshift=5, xrotation=30, yticks='Metrics', xticks=['BackTrans', 'EDA', 'SplitAug', 'SpellingAug', 'WordEmbs'])
