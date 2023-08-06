import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="charprinto",
    version="2.0.1",
    description="Print strings character by character easily",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="AverseABFun",
    author_email="averse.abfun@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["charprinto"],
    include_package_data=True,
    install_requires=["termcolor", "cursor","sys","os"],
    entry_points={
        "console_scripts": [
            "charprint=charprinto.__init__:charprint",
        ]
    },
)