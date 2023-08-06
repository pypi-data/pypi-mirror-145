from setuptools import setup

with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(
    name='NLIDataPrep',
    url='https://github.com/ygherman/NLIDataPrep',
    author="Yael Gherman",
    author_email="gh.gherman@gmail.com",
    version='0.0.1',
    description='Python Package for data preprocessing and preparation for REI prject metadata ingest',
    py_modules = [""],
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_require = [
        "pandas ~= 1.4",
    ],
    extras_require = {
        "dev": [
            "pytest>=3.8",
            "mock>=4.0.0"
        ],
    }
)

