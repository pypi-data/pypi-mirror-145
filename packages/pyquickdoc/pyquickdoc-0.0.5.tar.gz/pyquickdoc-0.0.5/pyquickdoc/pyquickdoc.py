#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
import tomd

from config.zh_dict import zh_dicts
from config.en_dict import en_dicts
from doctype.html_template import index

__date__ = "2022/04/03"
__author__ = ""
__website__ = "http://www.52phm.cn"


def cache(filename, func):
    out = sys.stdout
    sys.stdout = open(filename, "w", encoding='utf-8')
    help(func)
    sys.stdout = out
    # sys.stdout.close()


def chapter(cache_path):
    chapter_origin = []
    chapter_new = []
    chapter_name = []
    pattern = ["    " + '-'*(i+1) + '\n' for i in range(20)]
    with open(cache_path, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
        module_name = ''
        if re.search('module ', lines[0]):
            module_name = lines[0].split("module ")[-1].strip()[:-1]
        for i in range(1, len(lines)):
            if lines[i] in pattern:
                chapter_origin.append(lines[i-1])
                name = lines[i-1].strip()
                chapter_name.append(name)
                if chapter_name and name != chapter_name[0]:
                    chapter_new.append('<a name="{}"></a></div></div><h3>{}<br>'.format(name, name))
                else:  # 第一章节之前没有灰色背景
                    chapter_new.append('<a name="{}"></a><h3>{}<br>'.format(name, name))
    return chapter_origin, chapter_new, chapter_name, module_name


def func_apidoc(func, filename, title=None, return_type='html', zh_dict_diy=None, en_dict_diy=None):
    """自动生成python库的函数接口文档，支持生成文档到 html 及 md 文件

    对于

    """
    if title is None:
        title = ''
        if func.__name__:
            title += func.__name__

    # 先缓存到 md 文件中
    cache_path = func.__name__ + "_001.md"
    cache(cache_path, func)

    # 提取章节信息
    chapter_origin, chapter_new, chapter_name, module_name = chapter(cache_path)
    if module_name:
        title = module_name + '.' + title

    # 读取 txt 文件，对格式进行调整
    with open(cache_path, 'r', encoding='utf-8') as fp:
        func_name = func.__name__
        lines = fp.read()
        # 章节标题
        for i in range(len(chapter_new)):
            lines = lines.replace(chapter_origin[i], chapter_new[i])
        # 特殊字符处理
        lines = lines.replace("\n", "<br>")
        lines = lines.replace("        ", "&emsp;&emsp;")

        # 函数参数，设置黄色背景块
        try:
            func_top = 'Help on {}\)<br>    '.format(".*")
            func_top = re.findall(pattern=func_top, string=lines)[0].split("<br>    ")[0] + "<br>    "
            func_top_ = func_top.replace(":<br><br>", '<br><br><div style="background-color:#fbe54e">')
            func_top_ = func_top_ + "</div><br>"
            lines = lines.replace(func_top, func_top_)
        except:
            pass

        # 每一个章节，设置灰色背景
        for i in range(20):
            lines = lines.replace("<br>    {}<br>".format('-' * (i + 1)),
                                  '</h3><div style="background-color:#f2eadd;"><div style="margin-left:1.5em;">')
        # 目录列表
        menu_format = '<p style="text-align:left;line-height:25px;"><a href="#{}"><img src="http://www.52phm.cn/media/editor/reply.svg"> {}</a></p>'
        menu = [menu_format.format(i, i) for i in chapter_name]
        menu = "<br>".join(menu)

        # 结尾补齐
        lines = "<h3>{}</h3><br>".format(title) + lines + "</div></div><br><br><br>"

    os.remove(cache_path)

    if filename.split('.')[-1] == 'md':
        with open(filename, 'w', encoding='utf-8') as fp:
            fp.write(lines)
    if return_type == 'markdowm' or return_type == "md":
        return tomd.Tomd(lines).markdown

    if filename.split('.')[-1] == 'html':
        with open(filename, 'w', encoding='utf-8') as fp:
            lines = index.format(title, menu, lines)
            fp.write(lines)
    if return_type == 'html':
        lines = index.format(title, menu, lines)
        return lines


import numpy as np
import www52phmcn as phm
import pandas as pd
from sklearn import metrics


for i, v in enumerate([np.fft, np.fft.rfft, np.fft.rfftfreq, np.sign, np.sin, pd.DataFrame, pd.read_csv, pd.to_pickle,
                       metrics.auc, metrics.accuracy_score, metrics.classification_report, phm.generate_signal, phm.awgn]):
    func_apidoc(v, '{}.html'.format(i))
# func_apidoc(phm.generate_signal, 'aa.md')
# func_apidoc(pd.to_pickle, 'aa.md')

