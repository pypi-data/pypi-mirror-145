#!/usr/bin/env python
# coding=utf-8
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="utils_for_ds",
    version="0.0.15",
    author="ZhangLe",
    author_email="zhangle@gmail.com",
    description="common used functions for Data Scientist",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZhangLe59151/ds_utils",
    project_urls={
        "Bug Tracker": "https://github.com/ZhangLe59151/ds_utils",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages("."),
    install_requires = [
      'pandas>=0.25.1',
      'numpy>=1.21.5', 
      'DateTime>=4.4', 
      'tensorflow>=2.7.0',
      'xgboost>=1.5.2',
      'scikit-learn>=1.0',
      'keras-tcn>=3.4.0',
      'matplotlib>=3.1.1',
      'pickleshare>=0.7.5',
      'cloudpickle>=1.2.2',
      'optuna>=2.10.0',
      'seaborn>=0.9.0'],
    python_requires=">=3.6",
)