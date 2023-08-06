from setuptools import setup, find_packages
import codecs
import os


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '4.0.0'
DESCRIPTION = 'A Module For Managing and Creating DBs.'

# Setting up
setup(
    name="OsomeDB",
    version=VERSION,
    author="Merwin",
    author_email="<merwinmathews1001@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/mastercodermerwin/OSOME-DB",
    project_urls={
        "Bug Tracker": "https://github.com/mastercodermerwin/OSOME-DB/issues",
    },
    long_description=long_description,
    packages=find_packages(),
    install_requires=['cryptography', 'sty'],
    keywords=['python', 'DB','DataBase','Simple','Data','Manage','Create','nosql'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
