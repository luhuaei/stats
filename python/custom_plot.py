import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# custom color
colorreds_dict = {"鼠鼻红": "#e3b4b8", "春梅红": "#f1939c", "白芨红": "#de7897",
                  "艳红": "#ed5a65", "玉红": "#c04851", "茶花红": "#ee3f4d"}
colorreds_list = [x for x in colorreds_dict.values()]
colors_list = ["#f38181", "#fce38a", "#ffd3b6", "#95e1d3", "#28c3d4",
               "#11999e", "#574f7d", "#4f3a65"]


def bar_addlabel(rects, ax, xpos="center"):
    """Attach a text on every bar display it height.
    xpos indicates the offset. it has {center, left, right}"""

    ha = {"center": "center", "left": "right", "right": "left"}
    offset = {"center": 0, "left": -1, "right": 1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate("{:.2%}".format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),
                    textcoords="offset points",
                    ha=ha[xpos], va="bottom")
    return ax


def barh_addlabel(rects, ax):
    """barh plot add label on bar"""

    for rect in rects:
        width = rect.get_width()
        ax.annotate("{:.2%}".format(width),
                    xy=(width, rect.get_y()),
                    xytext=(3, 3),
                    textcoords="offset points",
                    ha="left", va="bottom")
    return ax


def double_index_bar(series, width, ax, label1, label2):
    """plot double index series bar plot, but base x axis is label1,
    iterate add label2, each iterate add one kind label2.
    比如，具有年龄与幸福感两个索引，以年龄为x轴，幸福感为y轴，每一次添加一种幸福感。
    """
    series = series.sort_index(level=0)
    index1 = series.index.levels[0]
    index2 = series.index.levels[1]
    n = len(index1)
    if n % 2 == 0:
        offset = 2*np.arange(int(-n/2), int(n/2))
    else:
        offset = 2*np.arange(int(-n/2), int(n/2) + 1)
    for o, ind2, lab2 in zip(offset, index2, label2):
        height = series.loc[:, ind2]
        height = height / height.sum()
        ax.bar(index1 + o*width/2, height, width, label=lab2)
    ax.set_xticks(index1)
    ax.set_xticklabels(label1)
    ax.legend()
    return ax


def double_index_bar1(series, width, ax, label1, label2):
    """plot double index series bar plot. And this function same use label1 as
    x axis, except add bar behavior. The function base label1 add all label2
    on once. In the other words, this function iterate add label1.

    比如，具有年龄与幸福感两个索引，以年龄为x轴，幸福感为y轴，每一次添加当前年龄对应的幸福感。
    """
    series = series.sort_index(level=0)
    index1 = series.index.levels[0]
    index2 = series.index.levels[1]
    n2 = len(index2)

    # 偏移量，指当同一x轴标签存在多个bar时，各个bar偏移的程度
    if n2 % 2 == 0:
        offset = 2*np.arange(int(-n2/2), int(n2/2))
    else:
        offset = 2*np.arange(int(-n2/2), int(n2/2) + 1)
    for i in index1:
        pos = i + offset*width/2
        height = series.loc[i, ]
        height = height / height.sum()
        index3 = height.index
        for ci, p, h, lab2 in zip(index3, pos, height, label2):
            ax.bar(p, h, width, color=colors_list[int(ci - 1)])
    ax.set_xticks(index1)
    ax.set_xticklabels(label1)
    ax.legend(label2)
    return ax
