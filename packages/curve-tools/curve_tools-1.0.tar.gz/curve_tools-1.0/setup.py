# coding: utf-8

from setuptools import setup, find_packages

setup(name='curve_tools',  #打包后的包文件名
    version='1.0',
    description='Tool set to analyze curve', #说明
    author='felix',
    author_email='qiyu_sjtu@163.com',
    url='',
    packages=find_packages(),
    py_modules=['curve.curve'],   #你要打包的文件如果要打包多个文件，慢慢添加吧
)