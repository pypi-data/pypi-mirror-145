# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="zapscrapper",
    version="0.0.3",
    url="",
    license="MIT License",
    author="Eduardo M. de Morais",
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email="emdemor415@gmail.com",
    keywords=["webscrapping", "imoveis"],
    description="This is a package to make webscrappng on zapimoveis.com.br",
    packages=["zapscrapper"],
    install_requires=[
        "BeautifulSoup4==4.10.0",
        "boto3==1.21.32",
        "sqlalchemy==1.4.34",
        "tqdm==4.63.1",
        "pandas==1.1.5",
    ],
)
