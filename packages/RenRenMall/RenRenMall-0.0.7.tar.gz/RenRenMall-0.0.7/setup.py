from setuptools import setup, find_packages

setup(
    name='RenRenMall',  # 应用名
    version='0.0.7',  # 版本号
    author='YarnBlue',
    author_email='zqb090325@126.com',
    description='人人商城后台管理',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True
)
