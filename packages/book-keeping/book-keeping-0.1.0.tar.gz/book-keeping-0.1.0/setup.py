import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="book-keeping",
    version="0.1.0",
    description="Track config and results for digital experiments.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jla-gardner/book-keeping",
    author="John Gardner",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    packages=["book_keeping"],
    keywords=["digital", "experiment", "record", "config"],
    install_requires=[],
    package_data={},
    python_requires=">=3.7, <4",
)
