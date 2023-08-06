from setuptools import setup,find_packages
setup(
    name="zjq-01",
    version="0.2",
    author="zjq",
    description="The members of this team are:钟佳棋，王思仁，黄楚洁",
    packages = find_packages("zjq"),
    package_dir = {"":"zjq"},
    package_data = {
        "":[".txt",".info","*.properties",".py"],
        "":["data/*.*"],
    },

    exclude = ["*.test","*.test.*","test.*","test"]
)


