from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='WeCom_nodream',  # 包名
        version='1.0.0',  # 版本号
        description='企业微信API',  # 简单描述
        long_description=long_description, # 详细描述
        author='noDream', # 作者
        author_email='1802024110@qq.com', # 作者邮箱
        url='https://github.com/1802024110/WeCom_API', # 项目地址
        install_requires=["requests"], # 安装依赖
        license='Apache License', # 许可证
        packages=find_packages(), # 包名
        platforms=["all"],  # 平台
        classifiers=[
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Natural Language :: Chinese (Simplified)',
            'Programming Language :: Python :: 3',
        ], # 分类
        )