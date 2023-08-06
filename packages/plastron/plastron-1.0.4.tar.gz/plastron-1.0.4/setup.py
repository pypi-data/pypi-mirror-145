"""Install packages as defined in this file into the Python environment."""
import pathlib
from setuptools import setup, find_namespace_packages, find_packages

# The version of this tool is based on the following steps:
# https://packaging.python.org/guides/single-sourcing-package-version/
VERSION = {}

with open("./src/plastron/__init__.py") as fp:
    # pylint: disable=W0122
    exec(fp.read(), VERSION)

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="plastron",
    author="Kavun Nuggihalli",
    author_email="kavunnuggihalli@gmail.com",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kavunnuggihalli/Plastron",
    description="An interactive shell library",
    version=VERSION.get("__version__", "0.0.0"),
    package_dir={"": "src"},
    packages=find_packages(
        where='src',
        include=['plastron*'],  # ["*"] by default
        exclude=['plastron.tests'],  # empty by default
    ),
    install_requires=[
        "setuptools>=45.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.0",
        "Topic :: Utilities",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.7",
        "Topic :: System :: Shells",
        "Topic :: System :: System Shells",
    ],
)
