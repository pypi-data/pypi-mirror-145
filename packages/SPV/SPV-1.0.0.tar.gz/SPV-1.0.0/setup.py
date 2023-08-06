from setuptools import setup, find_packages
import codecs
import os


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'SPV Secure Password Varification'

# Setting up
setup(
    name="SPV",
    version=VERSION,
    author="Merwin",
    author_email="<merwinmathews1001@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/mastercodermerwin/SPV-SecurePasswordVerification-",
    project_urls={
        "Bug Tracker": "https://github.com/mastercodermerwin/SPV-SecurePasswordVerification-/issues",
    },
    long_description=long_description,
    packages=find_packages(),
    install_requires=['cryptography'],
    keywords=['python', 'secure','password','varification','user','client'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
