from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(here + "/README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hiccupy",
    py_modules=["hiccupy"],
    version="1.0.0",
    description="Rendering HTML from hiccup-style lists in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rebecca Jackson",
    author_email="rbca.jackson@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
)
