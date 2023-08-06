import setuptools #导入setuptools打包工具
 
with open("src\\README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
 
setuptools.setup(
    name="tbse", # 用自己的名替换其中的YOUR_USERNAME_
    packages=['tbse'],
    package_dir={'tbse':'src'},
    install_requires=['tbutils','psmlc'],
    platforms=['nt','posix'],
    version=open('ver.txt').read(),    #包版本号，便于维护版本
    author="laman29",    #作者，可以写自己的姓名
    author_email="fzwxr@hotmail.com",    #作者联系方式，可写自己的邮箱地址
    description="tbutil simple edition",#包的简述
    long_description=long_description,    #包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="https://gitee.com/laman29/toolbox",    #自己项目地址，比如github的项目地址
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',    #对python的最低版本要求
)