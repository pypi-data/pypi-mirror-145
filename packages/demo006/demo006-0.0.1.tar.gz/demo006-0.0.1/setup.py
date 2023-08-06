from setuptools import setup, find_packages


setup(
    name='demo006',  # 对外我们模块的名字
    version='0.0.1',  # 版本号
    description='测试本地发布模块',  # 描述
    author='demo',  # 作者
    author_email='2374521450@qq.com',
    url="http://www.52phm.cn",
    packages=find_packages(),  # 要发布的模块
)
