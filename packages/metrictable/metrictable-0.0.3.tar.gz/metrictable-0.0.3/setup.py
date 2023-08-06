from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Description: metrics for regression'
LONG_DESCRIPTION = 'Long Description: metrics for regression'

# Setting up
setup(
    name="metrictable",
    version=VERSION,
    author="sarath babu",
    author_email="babusarath05@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    #install_requires=['sklearn','pandas'],
    keywords=['python', 'regression','metrics','adj r2_score','r2_score','rmse'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
