from setuptools import setup, find_packages

REQUIRED = ["pyquery", "qasync", "jinja2"]
setup(
    name = "mvvmQt" ,
    version = "0.11" ,
    description = "write qt like html" ,
    author = "Norman",
    author_email = "332535694@qq.com",
    url = "http://www.csdn.net",
    packages = find_packages(),
    python_requires = '>=3.6.0',
    install_requires = REQUIRED
)