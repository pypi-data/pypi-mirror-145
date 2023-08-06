# -*- coding: utf-8 -*-
from setuptools import setup,find_packages

with open("README.md",'r',encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tColorP',
    version='0.0.1',
    keywords='print with color',
    description='print with color',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ruxia-TJY",
    author_email="ruxia.tjy@qq.com",
    url="https://github.com/ruxia-TJY/TColorP",
    download_url="https://github.com/ruxia-TJY/TColorP",
    project_urls={
        "Bug Tracker":"https://github.com/ruxia-TJY/TColorP/issues",
    },
    install_requires=[],
    packages=find_packages(),
    license='MIT',
    python_requires='>=3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: MIT License'
    ]
)