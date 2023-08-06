#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re

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


def func_apidoc(func, filename, title=None, return_type='html', zh_dict_diy=None, en_dict_diy=None):
    """自动生成python库的函数接口文档，支持生成文档到 html 及 md 文件

    对于

    """
    if title is None:
        title = ''
        if func.__module__:
            title += func.__name__
        if func.__name__:
            title += '.' + func.__name__
    if zh_dict_diy is None:
        zh_dict_diy = zh_dicts
    if en_dict_diy is None:
        en_dict_diy = en_dicts

    # 先缓存到 md 文件中
    cache_path = func.__name__ + "_001.md"
    cache(cache_path, func)

    # 读取 txt 文件，对格式进行调整
    with open(cache_path, 'r', encoding='utf-8') as fp:
        lines = fp.read()
        # print(lines)
        lines = lines.replace("\n", "<br>")
        lines = lines.replace("        ", "&emsp;&emsp;")
        lines = lines.replace(":<br><br>", '<br><br><div style="background-color:#fbe54e">').\
            replace(")<br>", ")</div><br>")

        menu = []
        menu_li = '<p style="text-align:left;line-height:25px;"><a href="#{}"><img src="http://www.52phm.cn/media/editor/reply.svg"> {}</a></p>'
        # 中文版接口注释
        if re.search(pattern="    {}".format(zh_dict_diy['chapter_1']), string=lines):
            lines = lines.replace("    {}".format(zh_dict_diy['chapter_1']), "<a name={}></a><h3>{}</h3>".format(
                zh_dict_diy['chapter_1'], zh_dict_diy['chapter_1']))
            menu.append(menu_li.format(zh_dict_diy['chapter_1'], zh_dict_diy['chapter_1']))
        for i in zh_dict_diy['other_chapter']:
            if re.search(pattern="    {}".format(i), string=lines):
                menu.append(menu_li.format(i, i))
                lines = lines.replace("    {}".format(i), "<a name={}></a><h3>{}</h3>".format(i, i))
                lines = lines.replace("<h3>{}".format(i), '</div></div><h3>{}'.format(i))  # 除了第一个输入参数之外，后续加入的内容都要进行这一步

        # 英文版接口注释
        if re.search(pattern="    {}".format(en_dict_diy['chapter_1']), string=lines):
            lines = lines.replace("    {}".format(en_dict_diy['chapter_1']), "<a name={}></a><h3>{}</h3>".format(
                en_dict_diy['chapter_1'], en_dict_diy['chapter_1']))
            menu.append(menu_li.format(en_dict_diy['chapter_1'], en_dict_diy['chapter_1']))
        for i in en_dict_diy['other_chapter']:
            if re.search(pattern="    {}".format(i), string=lines):
                menu.append(menu_li.format(i, i))
                lines = lines.replace("    {}".format(i), "<a name={}></a><h3>{}</h3>".format(i, i))
                lines = lines.replace("<h3>{}".format(i), '</div></div><h3>{}'.format(i))  # 除了第一个输入参数之外，后续加入的内容都要进行这一步

        # 目录列表
        menu = "<br>".join(menu)

        # 每一个章节，设置灰色背景
        for i in range(20):
            lines = lines.replace("</h3><br>    {}<br>".format('-' * (i + 1)),
                                  '</h3><div style="background-color:#f2eadd;"><div style="margin-left:1.5em;">')

        # 结尾补齐
        lines = "<h3>{}</h3><br>".format(title) + lines + "</div></div><br><br><br>"

    os.remove(cache_path)

    if filename.split('.')[-1] == 'md':
        with open(filename, 'w', encoding='utf-8') as fp:
            fp.write(lines)
            pass
    if return_type == 'markdowm' or return_type == "md":
        return lines

    if filename.split('.')[-1] == 'html':
        with open(filename[:-2]+"html", 'w', encoding='utf-8') as fp:
            lines = index.format(title, menu, lines)
            fp.write(lines)
            pass
    if return_type == 'html':
        lines = index.format(title, menu, lines)
        return lines


