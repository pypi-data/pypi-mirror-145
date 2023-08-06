import setuptools


with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()


setuptools.setup(
    packages=setuptools.find_packages()
)