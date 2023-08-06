from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ofanalysis',
    version='0.2.8',
    packages=find_packages(),
    url='https://github.com/laye0619/ofanalysis',
    author='LayeWang',
    author_email='laye0619@gmail.com',
    description='A framework analysing open fund in China',
    include_package_data=True,
    install_requires=[
        "pandas",
        "loguru",
        "akshare",
        "tushare",
        "pymongo",
        "pytz",
        "requests",
        "pyecharts",
        "setuptools",
        "bs4",
        "beautifulsoup4",
        "selenium",
        "Pillow",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
