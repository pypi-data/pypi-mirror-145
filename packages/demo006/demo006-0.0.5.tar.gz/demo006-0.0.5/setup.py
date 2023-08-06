from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='demo006',  # 对外我们模块的名字
    author='china 52phm',  # 作者
    author_email='2374521450@qq.com',
    version='0.0.5',  # 版本号
    description='发布自己的第三方模块库测试...',  # 项目摘要
    long_description=long_description,  # 项目介绍
    long_description_content_type="text/markdown",
    url="http://www.52phm.cn",
    packages=find_packages(),  # 要发布的模块
    dependency_links=["http://www.52phm.cn/blog", "http://www.52phm.cn/info", "http://www.52phm.cn/"],
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
        "主页": "http://www.52phm.cn",
        "Download": "http://www.52phm.cn",
        "Documentation": "http://www.52phm.cn",
        "Source Code": "http://www.52phm.cn",
        "Homepage": "http://www.52phm.cn",
    },
)


