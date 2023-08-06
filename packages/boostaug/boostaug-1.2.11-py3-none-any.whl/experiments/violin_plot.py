# -*- coding: utf-8 -*-
# file: violin_plot.py
# time: 2022/1/11
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
# -*- coding: utf-8 -*-
# file: violin_plot.py
# time: 2021/10/31
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

import os
from findfile import find_cwd_files, find_cwd_file

import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib
from findfile import find_file


def acc_violin_plot():
    fast_lcf_acc = [[83.23, 84.01, 82.13, 82.97, 80.62],
                    [88.3, 88.04, 89.29, 88.55, 88.3],
                    [87.96, 88.52, 86.85, 87.04, 88.33],
                    [93.33, 93.66, 93.5, 93.82, 93.15]]

    fast_lcf_boost_acc = [[85.42, 84.8, 85.74, 84.95, 84.48],
                          [90.54, 90.27, 89.64, 90, 89.73],
                          [88.89, 89.26, 90, 89.07, 88.89],
                          [94.96, 94.31, 94.8, 94.47, 94.63]]

    # violin_parts = plt.violinplot(fast_lcf_acc, showmeans=True, showmedians=True, showextrema=True)
    #
    # for pc in violin_parts['bodies']:
    #     pc.set_facecolor('black')
    #     pc.set_edgecolor('black')
    #     pc.set_linewidth(2)

    boxs_parts1 = plt.boxplot(fast_lcf_acc, widths=0.5)

    for item in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
        plt.setp(boxs_parts1[item], color='grey')
    plt.setp(boxs_parts1["fliers"], markeredgecolor='grey')

    boxs_parts2 = plt.boxplot(fast_lcf_boost_acc, widths=0.5)

    for item in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
        plt.setp(boxs_parts2[item], color='black')
    plt.setp(boxs_parts2["fliers"], markeredgecolor='black')
    # plt.show()
    tikz_code = tikzplotlib.get_tikz_code()
    tex_src = acc_violin_template.replace('$src_code$', tikz_code)
    tex_src = tex_src.replace(r'\definecolor{color0}{rgb}{0.12156862745098,0.566666666666667,0.705882352941177}',
                              r'\definecolor{color0}{rgb}{0.28, 0.24, 0.2}')
    tex_name = '{}-violin.tex'.format('Acc')
    open(tex_name, mode='w', encoding='utf8').write(tex_src)

    plt.close()


def f1_violin_plot():
    fast_lcf_f1 = [[79.68, 80.93, 78.74, 79.3, 77.37],
                   [82.27, 82.61, 83.85, 82.8, 81.97],
                   [73.42, 75.44, 71.2, 73.09, 75.32],
                   [80.5, 81.17, 80.88, 81.56, 80.03]]
    fast_lcf_boost_f1 = [[82.79, 81.91, 83.19, 82.22, 81.28],
                         [85.94, 85.66, 83.99, 85.09, 84.45],
                         [76.87, 77.7, 77.97, 77.27, 78.57],
                         [82.83, 83.91, 86, 83.02, 83.42]]

    # violin_parts = plt.violinplot(fast_lcf_f1, showmeans=True, showmedians=True, showextrema=True)

    # for pc in violin_parts['bodies']:
    #     pc.set_facecolor('black')
    #     pc.set_edgecolor('black')
    #     pc.set_linewidth(1)

    boxs_parts1 = plt.boxplot(fast_lcf_f1, widths=0.5)

    for item in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
        plt.setp(boxs_parts1[item], color='grey')
    plt.setp(boxs_parts1["fliers"], markeredgecolor='grey')

    boxs_parts2 = plt.boxplot(fast_lcf_boost_f1, widths=0.5)

    for item in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
        plt.setp(boxs_parts2[item], color='black')
    plt.setp(boxs_parts2["fliers"], markeredgecolor='black')

    # plt.show()
    tikz_code = tikzplotlib.get_tikz_code()
    tex_src = f1_violin_template.replace('$src_code$', tikz_code)
    tex_src = tex_src.replace(r'\definecolor{color0}{rgb}{0.12156862745098,0.566666666666667,0.705882352941177}',
                              r'\definecolor{color0}{rgb}{0.28, 0.24, 0.2}')
    tex_name = '{}-violin.tex'.format('F1.pdf')
    open(tex_name, mode='w', encoding='utf8').write(tex_src)

    plt.close()


if __name__ == '__main__':
    acc_violin_template = r"""
    \documentclass{article}
    \usepackage{pgfplots}
    \usepackage{tikz}
    \usepackage{caption}
    \usetikzlibrary{intersections}
    \usepackage{helvet}
    \usepackage[eulergreek]{sansmath}
    \usepackage{amsfonts,amssymb,amsmath,amsthm,amsopn}	% math related

    \begin{document}
        \pagestyle{empty}
            \pgfplotsset{ compat=1.12,every axis/.append style={
                font = \normalsize,
                grid = major,
                thick,
                xtick={1,2,3,4},
                xticklabels={Laptop14, Restaurant14, Restaurant15, Restaurant16},
                ylabel = {Accuracy.pdf},
                xlabel = {Dataset},
                x tick label style={rotate=15,anchor=north},
                xticklabel shift=1pt,
                line width = 1pt,
                tick style = {line width = 0.8pt}}}
        \pgfplotsset{every plot/.append style={thin}}


    \begin{figure}
    \centering

    $src_code$

    \end{figure}

    \end{document}

    """

    f1_violin_template = r"""
       \documentclass{article}
       \usepackage{pgfplots}
       \usepackage{tikz}
       \usepackage{caption}
       \usetikzlibrary{intersections}
       \usepackage{helvet}
       \usepackage[eulergreek]{sansmath}
       \usepackage{amsfonts,amssymb,amsmath,amsthm,amsopn}	% math related

       \begin{document}
           \pagestyle{empty}
               \pgfplotsset{ compat=1.12,every axis/.append style={
                   font = \normalsize,
                   grid = major,
                   thick,
                   xtick={1,2,3,4},
                   xticklabels={Laptop14, Restaurant14, Restaurant15, Restaurant16},
                   ylabel = {F1.pdf},
                   xlabel = {Dataset},
                   x tick label style={rotate=15,anchor=north},
                   xticklabel shift=1pt,
                   line width = 1pt,
                   tick style = {line width = 0.8pt}}}
           \pgfplotsset{every plot/.append style={thin}}


       \begin{figure}
       \centering

       $src_code$

       \end{figure}

       \end{document}

       """

    acc_violin_plot()

    f1_violin_plot()

    texs = find_cwd_files('.tex')
    for pdf in texs:
        cmd = 'pdflatex "{}" "{}.crop.pdf"'.format(pdf, pdf).replace(os.path.sep, '/')
        os.system(cmd)

    pdfs = find_cwd_files('.pdf', exclude_key='crop')
    for pdf in pdfs:
        cmd = 'pdfcrop "{}" "{}.crop.pdf"'.format(pdf, pdf).replace(os.path.sep, '/')
        os.system(cmd)

    # for f in find_cwd_files(['.tex']) + find_cwd_files(['.aux']) + find_cwd_files(['.log']) + find_cwd_files(['.pdf'], exclude_key='crop'):
    #     os.remove(f)
    for f in find_cwd_files(['.aux']) + find_cwd_files(['.log']) + find_cwd_files(['.pdf'], exclude_key='crop'):
        os.remove(f)
