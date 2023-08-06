from pathlib import Path

from setuptools import setup

setup(
    name="random_readline",
    version="0.1.0",
    packages=["random_readline"],
    author="Yuhsak Inoue",
    author_email="yuhsak.inoue@gmail.com",
    maintainer="Yuhsak Inoue",
    maintainer_email="yuhsak.inoue@gmail.com",
    license="MIT",
    url="https://github.com/yuhsak/random-readline",
    download_url="https://github.com/yuhsak/random-readline",
    description="Randomized fast readline for large text files.",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
)
