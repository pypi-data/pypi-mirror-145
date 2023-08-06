"""setup script"""

from setuptools import setup

with open("version.txt", "r", encoding="UTF-8") as version_file:
    version = version_file.read()

with open("README.md", "r", encoding="UTF-8") as readme_file:
    readme = readme_file.read()

DEPENDENCIES = ["pandas", "XlsxWriter", "setuptools"]

setup(
    name="pandas-excel",
    version=version,
    author="Christopher Hacker",
    author_email="hackerlikecomputer@gmail.com",
    url="https://github.com/christopher-hacker/pandas-excel",
    description="quickly turn pandas dataframes into shareable Excel reports",
    long_description=readme,
    long_description_content_type="text/markdown",
    package_dir={"excel": "excel"},
    packages=["excel", "excel.write", "excel.format", "excel.common"],
    install_requires=DEPENDENCIES,
    setup_requires=DEPENDENCIES,
)
