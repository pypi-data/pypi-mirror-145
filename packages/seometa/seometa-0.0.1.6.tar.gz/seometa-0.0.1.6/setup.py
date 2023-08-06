from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open('README.md', 'r', encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.1.6'
DESCRIPTION = 'Get SEO Meta-data from Websites'
# LONG_DESCRIPTION = 'A package that allows get metadata from websites allowing to perfect your targeting.'

# Setting up
setup(
    name="seometa",
    version=VERSION,
    author="Aymane Elhattab",
    author_email="<aymane.elhattab.master@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['beautifulsoup4', 'requests'],
    keywords=['seo', 'meta data', 'website', 'data scraper', 'data', 'data mining'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
