#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re

from doctype.html_template import index

"""
@date："2022/04/03"
@author："Liang XiaoZhi"
@website："http://www.52phm.cn"
"""


def cache(filename, func):
    """文件缓存

    主要是在本地短暂缓存，提取好文档信息后，将自动删除

    输入参数
    ---------
    filename，string，必选
        缓存路径

    func，function，必选
        需要查询文档的函数

    """
    out = sys.stdout
    sys.stdout = open(filename, "w", encoding='utf-8')
    help(func)
    sys.stdout = out
    # sys.stdout.close()


def chapter(cache_path):
    """获取章节标题

    输入参数
    ----------
    cache_path，string，必选
        缓存文件的文件名称

    输出参数
    ----------
    chapter_origin，list，
        原始章节字符串信息

    chapter_new，list
        处理格式后的章节字符串信息

    chapter_name, list
        章节名称列表

    module_name，string
        当前函数的模块路径

    """
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


def func_apidoc(func, filename=None, title=None, is_export=True, doctype='html'):
    """Python 函数注释接口文档生成

    Python 库的函数接口文档,支持快速生成,并且支持导出 html 与 markdown 文档

    输入参数
    ----------
    func：function，必选
        需要查询的目标函数，请注意此处输入是函数，后面不需要带上括号，也不是字符串名称

    filename：string，可选
        导出文件的路径与格式，如 d:/mydoc.html 或者 d:/mydoc.md，默认为 None，
        如果为 None，文档导出和返回文件格式将以 doctype 指定类型为准，并且文件名称以函数模块包路径命令，如 numpy.fft.rfft.html
        否则文档导出和返回文件格式将以 filename 指定类型为准

    title：string，可选
        文档标题，默认为 None 时将默认使用当前函数的模块包路径名称为文档标题，如 numpy.fft.rfft

    is_export：bool，可选
        表示是否保存接口文档为文件，默认为 True，不希望导出则可以设置为 False（不导出文件，但返回接口文档）

    doctype：string，可选
        导出文档的类型，只在 filename 为空时才发挥作用

    输出参数
    ----------
    apidoc：string[html]，string[md]
        返回当前查询函数的接口文档，

    参考样例
    ----------
    >>> import pyquickdoc as pdoc
    >>> pdoc.func_apidoc(pdoc.func_apidoc)  # 默认参数
    ### pyquickdoc.func_apidoc

    Help on function func_apidoc in module main
    func_apidoc(func, filename=None, title=None, is_export=True, doctype='html')

    Python 函数注释接口文档生成
    Python 库的函数接口文档,支持快速生成,并且支持导出 html 与 markdown 文档
    ...

    >>> import numpy as np
    >>> rfft_doc = pdoc.func_apidoc(np.fft.rfft, is_export=False)  # 只在程序中获取，不保存接口文档
    numpy.fft.rfft

    Help on function rfft in module numpy.fft
    rfft(a, n=None, axis=-1, norm=None)

    Compute the one-dimensional discrete Fourier Transform for real input.
    ...

    >>> import pandas as pd
    >>> pdoc.func_apidoc(pd.read_csv, doctype='md')  # 导出接口文档为 md 文件
    省略......
    """
    # 参数初始化
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
    if filename is None:  # 如果 filename 为空，默认以 doctype 指定格式导出文档，否则，doctype 要调整与 filename 的导出格式一致
        filename = title + '.' + doctype
    else:
        doctype = filename.split('.')[-1]

    # 读取文件，对格式进行调整
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

    if filename.split('.')[-1] == 'md' and is_export:
        with open(filename, 'w', encoding='utf-8') as fp:
            fp.write(lines)
    if doctype == 'markdowm' or doctype == "md":
        return lines

    if filename.split('.')[-1] == 'html' and is_export:
        with open(filename, 'w', encoding='utf-8') as fp:
            lines = index.format(title, menu, lines)
            fp.write(lines)
    if doctype == 'html':
        lines = index.format(title, menu, lines)
        return lines


