import os.path
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.rst")) as fid:
    README = fid.read()

setup(
      name="algomojo-kambala",
      version="1.0",
     description="A functional python wrapper for algomojo trading api",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://algomojo.com/docs/python",
    author="Algomojo",
    author_email="support@algomojo.com",
    license="MIT",
     packages=find_packages('kambala'),
    package_dir={'': 'kambala'},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],

    install_requires=[
        "requests"
    ],
)
