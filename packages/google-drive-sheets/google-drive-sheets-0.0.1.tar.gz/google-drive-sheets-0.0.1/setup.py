from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.1"
DESCRIPTION = "Google Drive and Sheets API utilities"
LONG_DESCRIPTION = "A utility for Google Drive and Sheets APIs that " \
                   "helps you create folders, spreadsheets and read/save data"

# Setting up
setup(
    name="google-drive-sheets",
    version=VERSION,
    author="Nishant Parmar",
    author_email="<nish240893@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'google-api-python-client',
                      'google-auth-httplib2', 'google-auth-oauthlib',
                      'requests', 'xlrd', 'openpyxl', 'oauth2client'],
    keywords=['python', 'google drive', 'google sheets', 'gsuite'],
    classifiers=[
        "Development Status :: 1 - Development",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
