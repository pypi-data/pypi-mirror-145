import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="technicalindicator",
    version="0.0.1",
    author="Nguyen Truong Long",
    author_email="contact@nguyentruonglong.com",
    description="The TechnicalIndicator library provides a set of technical indicators used by traders in Python",
    long_description="The TechnicalIndicator library provides a set of technical indicators used by traders in Python",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
    'pandas>=1.4.2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)