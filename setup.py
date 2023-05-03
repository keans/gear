from setuptools import setup, find_packages
from pathlib import Path


# get current directory
current_directory = Path(__file__).resolve().parent


def get_long_description():
    """
    get long description from README.rst file
    """
    with current_directory.joinpath("README.rst").open() as f:
        return f.read()


setup(
    name="gear",
    version="0.0.1",
    description="Generic analysis framework.",
    long_description=get_long_description(),
    url="https://github.com/keans/gear",
    author="Ansgar Kellner",
    author_email="keans@gmx.de",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    keywords="gear",
    packages=find_packages(
        exclude=["contrib", "docs", "tests"]
    ),
    install_requires=[
        "pyyaml", "cerberus", "python-dotenv", "click",
        "pandas", "dpkt", "xlrd", "openpyxl", "luigi",
        "python-powerstrip", "jinja2", "transitions",
        "nested-dict"
    ],
    extra_require={
        "docs": ["mkdocs"],
    },
    entry_points={
        "console_scripts": [
            "wrench=gear.cmds.wrench:cli"
        ],
    }
)
