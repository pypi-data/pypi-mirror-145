from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='demo006',  # 对外我们模块的名字
    author='demo',  # 作者
    author_email='2374521450@qq.com',
    version='0.0.2',  # 版本号
    description='测试本地发布模块',  # 项目摘要
    long_description=long_description,  # 项目介绍
    long_description_content_type="text/markdown",
    url="http://www.52phm.cn",
    packages=find_packages(),  # 要发布的模块
)
