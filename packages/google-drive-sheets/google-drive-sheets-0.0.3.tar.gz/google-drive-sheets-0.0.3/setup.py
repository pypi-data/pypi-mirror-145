from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.3"
DESCRIPTION = "Google Drive and Sheets API utilities"
LONG_DESCRIPTION = """
A utility for Google Drive and Sheets APIs that helps you create folders, 
spreadsheets and read/save data. 
Prerequisites: Before executing anything, please go through the steps here: 
(https://developers.google.com/drive/api/v3/quickstart/python). 
It will kickstart the authorization process for your own app. ave the 
`credentials.json` file (not saved in this repo) generated from the first 
step, in the parent directory to enable Google Drive and Sheets capabilities.
"""

# Setting up
setup(
    name="google-drive-sheets",
    version=VERSION,
    author="Nishant Parmar",
    author_email="<nish240893@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'google-api-python-client',
                      'google-auth-httplib2', 'google-auth-oauthlib',
                      'requests', 'xlrd', 'openpyxl', 'oauth2client'],
    keywords=['python', 'google drive', 'google sheets', 'gsuite'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
