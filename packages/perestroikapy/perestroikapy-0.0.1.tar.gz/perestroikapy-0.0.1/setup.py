import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="perestroikapy",
    version="0.0.1",
    packages=setuptools.find_packages()
)