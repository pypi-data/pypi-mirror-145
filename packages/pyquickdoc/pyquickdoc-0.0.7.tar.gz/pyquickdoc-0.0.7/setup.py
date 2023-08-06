"""
@date："2022/04/03"
@author："Liang XiaoZhi"
@website："http://www.52phm.cn"
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pyquickdoc',  # 对外我们模块的名字
    author='Liang XiaoZhi',  # 作者
    author_email='2374521450@qq.com',  # 作者邮箱
    version='0.0.7',  # 版本号
    description='Python 库的函数接口文档,支持快速生成,并且支持导出 html 与 markdown 文档',  # 项目摘要
    long_description=long_description,  # 项目介绍
    long_description_content_type="text/markdown",
    url="http://www.52phm.cn",  # 程序主页地址
    packages=find_packages(),  # 要发布的模块
    license="Apache",  # 协议（请注意按实际情况选择不同的协议），可选
    # 此处添加任意多个项目链接
    project_urls={
        "主页(Homepage)": "http://www.52phm.cn",
    },
    include_package_data=True,

)
