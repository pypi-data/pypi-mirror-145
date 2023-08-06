import pathlib
from setuptools import setup

here = pathlib.Path(__file__).parent
readme = (here / "README.md").read_text()

setup(
    name = "PyBj",
    version = "1.0.220404.0001",
    description = "PyBj (Python Blackjack)",
    long_description = readme,
    long_description_content_type = "text/markdown",
    url = "https://github.com/destrianto/pybj",
    download_url = "https://github.com/destrianto/pybj/releases/download/1.0.220404.0001/malas_1.0.220404.0001.zip",
    author = "Ade Destrianto",
    author_email = "ade.destrianto@mail.ru",
    license = "MIT",
    classifiers = [
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Topic :: Games/Entertainment"
    ],
    keywords = [
        "blackjack",
        "games"
    ],
    packages = [
        "pybj"
    ],
    python_requires = ">=3.9"
)