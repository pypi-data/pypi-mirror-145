# -*- coding: utf-8 -*-
# file: aug_range_traj.py
# time: 30/01/2022
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import os

import matplotlib
import matplotlib.pyplot as plt

import numpy
import numpy as np
import tikzplotlib
from findfile import find_file, find_cwd_files


# width, height = 10, 7
# plt.rcParams['figure.figsize'] = width, height


def legend_without_duplicate_labels(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    ax.legend(*zip(*unique))


def traj_plot():
    laptop14_acc = [[80.41, 79.78, 81.03, 80.09, 79.62, 80.56, 80.88, 79.94, 79.47, 79.78, 74.77, 71.93, 73.54, 72.3, 72.68],
                    [79.62, 80.09, 80.72, 79.78, 81.35, 80.88, 81.03, 79.62, 78.84, 80.72, 78.53, 80.72, 79.47, 79, 79.94],
                    [79.47, 81.03, 79.31, 79.47, 80.09, 80.25, 79.62, 79, 79.62, 80.09, 79.94, 79.78, 80.25, 80.25, 80.25],
                    [80.72, 80.09, 79.62, 80.88, 80.56, 79.47, 80.41, 80.72, 79.62, 79.47, 79.62, 79.94, 80.25, 80.88, 80.88],
                    [79.94, 80.25, 79.47, 80.88, 79.94, 80.56, 80.41, 79, 79.78, 79.94, 80.56, 80.88, 80.72, 79.78, 80.25],
                    [80.56, 80.09, 79.78, 79.15, 80.09, 80.25, 80.09, 80.88, 79.47, 78.84, 80.56, 79.94, 79.94, 79.94, 79.31],
                    [79.94, 81.5, 81.82, 80.72, 81.03, 81.66, 80.25, 80.09, 80.09, 80.56, 79.78, 80.56, 79.31, 80.25, 80.72],
                    [80.56, 80.88, 80.56, 80.41, 79.94, 79.31, 80.88, 78.84, 79.62, 80.09, 79.47, 81.03, 81.03, 80.72, 80.09],
                    [79.47, 80.25, 80.72, 79.15, 80.88, 79.15, 80.09, 79.78, 81.03, 80.41, 80.72, 80.09, 79.94, 80.56, 80.25],
                    [79.78, 80.09, 79.78, 80.25, 80.41, 79.78, 80.09, 79.78, 80.25, 80.41, 80.09, 80.41, 80.41, 79.94, 79.62]]
    laptop14_f1 = [[76.79, 75.49, 77.92, 77.21, 75.63, 76.96, 77.44, 76.26, 76.35, 76.12, 76.12, 76.78, 75.64, 77.31, 73.79],
                   [76.12, 75.99, 77.85, 76.43, 77.97, 77.46, 76.93, 76.04, 74.64, 76.9, 75.03, 77.46, 76.3, 75.89, 75.85],
                   [75.83, 77.19, 76.12, 76.27, 75.93, 77.19, 75.96, 75.34, 75.8, 76.71, 76.08, 76.99, 77.16, 76.79, 77.23],
                   [77.26, 76.04, 76.3, 77, 76.97, 75.78, 76.69, 77.01, 76.55, 75.73, 76.57, 75.95, 76.34, 77.51, 77.67],
                   [76.24, 76.65, 76.21, 77.34, 76.35, 77.4, 76.91, 75.03, 75.75, 76.5, 77.56, 77.3, 77.03, 76.57, 77.29],
                   [77.01, 76.46, 76.18, 75.83, 76.56, 76.41, 76.67, 77.92, 76.05, 75.13, 77.56, 76.05, 75.8, 76.74, 75.97],
                   [75.98, 78.49, 78.88, 77.54, 77.22, 78.46, 77.3, 76.65, 76.4, 76.59, 75.92, 77.89, 76.39, 77.18, 77.11],
                   [77.34, 77.5, 77.16, 76.93, 77.07, 75.75, 77.21, 75.06, 76.41, 76.34, 76.45, 77.77, 77.59, 76.62, 76.47],
                   [75.75, 77.32, 77.14, 75.95, 77.77, 75.58, 76.74, 76.37, 77.59, 77.11, 77.14, 77.22, 76.75, 76.89, 77.4],
                   [76.14, 76.9, 76.84, 76.49, 77.23, 76.14, 76.9, 76.84, 76.49, 77.23, 76.6, 76.43, 76.89, 76.45, 75.94]]

    rest15_acc = [[84.81, 85.19, 84.81, 85.74, 85, 85.19, 84.26, 85.93, 85.37, 85.19, 84.81, 84.44, 85.19, 84.44, 83.52],
                  [84.81, 85.19, 85.93, 85.37, 85.37, 85.19, 84.63, 84.81, 85.74, 85.19, 84.81, 85, 84.81, 85.37, 85],
                  [85.37, 85.19, 84.63, 85.74, 85, 84.63, 85.56, 86.3, 86.11, 85.37, 85.74, 85.93, 86.67, 85, 85],
                  [86.11, 83.52, 84.81, 84.81, 85.19, 85.74, 85.37, 85.37, 85.56, 84.81, 84.81, 86.3, 85.37, 85.74, 86.48],
                  [84.81, 85.74, 84.81, 85, 85.74, 85.74, 85, 86.11, 84.26, 85.93, 85.19, 85.74, 85.74, 86.11, 85.74],
                  [85.56, 86.11, 85.93, 86.11, 85, 86.48, 86.48, 85, 85.56, 84.81, 85, 85.56, 85.56, 85.37, 85.74],
                  [86.3, 85.37, 85.93, 85.74, 85.93, 85.19, 84.63, 86.11, 85.19, 85.19, 85.93, 85.74, 85.19, 85.19, 85.93],
                  [85.74, 86.67, 85, 86.11, 85.37, 86.67, 85.56, 85.37, 85.56, 85.74, 85.19, 85.74, 85.74, 85.37, 85],
                  [86.48, 86.11, 86.3, 85.74, 85.93, 86.3, 86.11, 86.3, 85.74, 85.93, 85.74, 85.93, 85.93, 85.56, 85],
                  [87.41, 84.81, 85.19, 85.74, 85.93, 87.41, 84.81, 85.19, 85.74, 85.93, 85, 85.56, 85.19, 85.74, 85.93]]
    rest15_f1 = [[72.49, 72.72, 72.97, 72.72, 72.47, 74.77, 71.93, 73.54, 72.3, 72.68, 71.09, 71.39, 73.79, 73.71, 70.65],
                 [71.35, 72.96, 73.07, 71.88, 71.28, 72.29, 72.94, 72.66, 73.85, 71.92, 71.65, 73.42, 74.02, 72.29, 73.59],
                 [74, 72.98, 71.84, 73.57, 73.64, 72.23, 72.48, 74.22, 74.86, 72.98, 74.09, 74.81, 72.25, 73.43, 72.31],
                 [75.22, 67.48, 73.2, 73.85, 72.59, 73.43, 73.85, 73.81, 73.78, 72.35, 73.35, 74.64, 73.8, 73.29, 73.44],
                 [71.65, 73.39, 72.67, 72.49, 72.67, 74.09, 74.16, 75.49, 73.82, 75.57, 73.07, 74.47, 73.34, 76.08, 72.85],
                 [74.47, 74, 73.58, 74.5, 73.19, 75.19, 74.63, 74.17, 73.49, 73.95, 72.99, 71.93, 74.76, 74.2, 75.7],
                 [74.7, 74.65, 73.66, 75.24, 73.97, 74.05, 72.41, 73.33, 72.29, 74.19, 75.81, 73.84, 73.1, 72.43, 74.34],
                 [74.55, 76.65, 74.1, 75.18, 74.92, 76.48, 75.85, 73.47, 74.23, 72.93, 72.78, 73.15, 73.74, 74.75, 72.93],
                 [74.12, 77.99, 75.33, 73.85, 74.76, 74.67, 77.99, 75.33, 73.85, 74.76, 74.08, 74.52, 74.45, 74.92, 74.43],
                 [75.68, 72.01, 73.89, 75.31, 76.6, 75.68, 72.01, 73.89, 75.31, 76.6, 73.07, 73.02, 73.89, 75.31, 76.6]]

    rest15_acc = np.array(rest15_acc)
    rest15_f1 = np.array(rest15_f1)
    laptop14_acc = np.array(laptop14_acc)
    laptop14_f1 = np.array(laptop14_f1)

    epoch = list(range(1, 11))
    ax = plt.subplot()
    l2 = ax.plot(epoch,
                 np.average(laptop14_f1, axis=1),
                 'D-',
                 color='deepskyblue',
                 markersize=4,
                 label='Laptop14-F1.pdf'
                 )
    ax.plot(epoch,
            laptop14_f1,
            'D',
            color='deepskyblue',
            markersize=4,
            )

    plt.fill_between(epoch,
                     np.average(laptop14_f1, axis=1) - np.std(laptop14_f1, axis=1),
                     np.average(laptop14_f1, axis=1) + np.std(laptop14_f1, axis=1),
                     alpha=0.3,
                     color='deepskyblue',
                     # hatch='/'
                     )

    l4 = ax.plot(epoch,
                 np.average(rest15_f1, axis=1),
                 '*-',
                 color='violet',
                 markersize=4,
                 label='Restaurant15-F1.pdf')
    ax.plot(epoch,
            rest15_f1,
            '*',
            color='violet',
            markersize=4)
    plt.fill_between(epoch,
                     np.average(rest15_f1, axis=1) - np.std(rest15_f1, axis=1),
                     np.average(rest15_f1, axis=1) + np.std(rest15_f1, axis=1),
                     color='violet',
                     alpha=0.3,
                     )

    l1 = ax.plot(epoch,
                 np.average(laptop14_acc, axis=1),
                 'x-',
                 color='lawngreen',
                 markersize=4,
                 label='Laptop14-Acc')
    ax.plot(epoch,
            laptop14_acc,
            'x',
            color='lawngreen',
            markersize=4)
    plt.fill_between(epoch,
                     np.average(laptop14_acc, axis=1) - np.std(laptop14_acc, axis=1),
                     np.average(laptop14_acc, axis=1) + np.std(laptop14_acc, axis=1),
                     color='lawngreen',
                     alpha=0.3,
                     )

    l3 = ax.plot(epoch,
                 np.average(rest15_acc, axis=1),
                 '^-',
                 color='darkorange',
                 markersize=4,
                 label='Restaurant15-Acc')
    ax.plot(epoch,
            rest15_acc,
            '^',
            color='darkorange',
            markersize=4)
    plt.fill_between(epoch,
                     np.average(rest15_acc, axis=1) - np.std(rest15_acc, axis=1),
                     np.average(rest15_acc, axis=1) + np.std(rest15_acc, axis=1),
                     color='darkorange',
                     alpha=0.3,
                     )

    plt.grid()
    plt.minorticks_on()
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # plt.tight_layout()
    ax.grid()
    ax.minorticks_on()

    legend_without_duplicate_labels(ax)
    # plt.legend(fontsize=11)
    # plt.show()

    tikz_code = tikzplotlib.get_tikz_code()
    tex_src = tex_template.replace('$src_code$', tikz_code).replace('$metric$', 'F1.pdf')
    # tex_src = tex_src.replace('\\addlegendentry{Laptop14-F1.pdf}', '', 15)
    # lines = tex_src.split('\n')
    # lines = lines[0:152] + lines[377:1199] + lines[152:377] + lines[1199:]
    # tex_src = '\n'.join(lines)
    tex_name = 'aug_range_traj.tex'.format()
    open(tex_name, mode='w', encoding='utf8').write(tex_src)

    plt.close()


if __name__ == "__main__":
    tex_template = r"""
\documentclass{article}
\usepackage{pgfplots}
\usepackage{tikz}
\usetikzlibrary{intersections}
\usepackage{helvet}
\usepackage[eulergreek]{sansmath}

\begin{document}
\pagestyle{empty}

\pgfplotsset{every axis/.append style={
	font = \normalsize,
	grid = major,
    ylabel = {Metric},
	xlabel = {\# of Augmentations},
	thick,
	line width = 0.8pt,
	tick style = {line width = 0.8pt}}
}
\pgfplotsset{every plot/.append style={very thin}}

\begin{figure}
\centering

$src_code$

\end{figure}

\end{document}

"""
    traj_plot()

    texs = find_cwd_files('.tex')
    for pdf in texs:
        cmd = 'pdflatex "{}"'.format(pdf).replace(os.path.sep, '/')
        os.system(cmd)

    pdfs = find_cwd_files('.pdf', exclude_key='crop')
    for pdf in pdfs:
        cmd = 'pdfcrop "{}" "{}"'.format(pdf, pdf).replace(os.path.sep, '/')
        os.system(cmd)

    for f in find_cwd_files(['.aux']) + find_cwd_files(['.log']) + find_cwd_files(['crop']):
        os.remove(f)
