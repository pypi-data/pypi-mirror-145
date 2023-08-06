import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="icdcrawl",
    version="0.0.0",
    description="ICD code crawler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sunrimii/icdcrawl",
    author="sunrimii",
    author_email="sunrimii@gmail.com",
    keywords="ICD-10, ICD-9, icd10data, icd9data, crawler",
    packages=find_packages(),
    python_requires=">=3.10, <4",
)
