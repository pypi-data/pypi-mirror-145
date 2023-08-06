from setuptools import setup, find_packages

setup(
    name="helloljj 0.1.1",
    version="0.1.1",
    description="the team 's member just only one  ",
    long_description="the lead of the team is lijiajun",

    author="ljj",
    author_email="1498283571@qq.com",

    packages = find_packages("src"),
    package_dir = {"":"src"},
    package_data = {
        # 定义打包除了 .py 之外的文件类型，此处 .py 其实可以不写
        "":[".txt",".info","*.properties",".py"],
        # 包含 data 文件夹下所有的 *.dat 文件
        "":["data/*.*"],
    },
    # 取消所有测试包
    exclude = ["*.test","*.test.*","test.*","test"]
    # include_package_data = True,
    # platforms = "any",
    # install_requires = []
)