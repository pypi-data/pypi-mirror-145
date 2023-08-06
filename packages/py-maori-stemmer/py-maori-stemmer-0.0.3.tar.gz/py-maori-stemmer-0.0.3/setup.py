import setuptools
from codecs import open


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-maori-stemmer",
    version="0.0.3",
    author="Yukio Fukuzawa",
    author_email="nishinokaze8@gmail.com",
    description="Stemmer for Maori language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fzyukio/py-maori-stemmer",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)