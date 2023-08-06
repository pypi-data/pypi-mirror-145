import setuptools
from WeiXinPaySDK.version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WeiXinPaySDK",
    version=__version__,
    author="navysummer",
    author_email="navysummer@yeah.net",
    description="WeiXinPaySDK是基于微信支付开发的sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/navysummer/WeiXinPaySDK.git",
    packages=setuptools.find_packages(exclude=["demo"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    platforms='python',
    install_requires=[
        "requests~=2.27.1",
        "xmltodict~=0.12.0",
        "qrcode~=7.3.1",
        "Pillow~=9.0.1",
        "lxml~=4.8.0",
        "cryptography~=36.0.2"
    ]

)

"""
1、打包流程
打包过程中也可以多增加一些额外的操作，减少上传中的错误

# 先升级打包工具
pip install --upgrade setuptools wheel twine

# 打包
python setup.py sdist bdist_wheel

# 检查
twine check dist/*

# 上传pypi
twine upload dist/*
# 安装最新的版本测试
pip install -U WeiXinPaySDK -i https://pypi.org/simple
"""
