"""Install packages as defined in this file into the Python environment."""
import pathlib
from setuptools import setup, find_namespace_packages, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="plastron",
    packages=['plastron'],
    description="An interactive shell library",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Kavun Nuggihalli",
    author_email="kavunnuggihalli@gmail.com",
    url="https://github.com/kavunnuggihalli/Plastron",
    keywords="python3 interactive shell library",
    project_urls={
        'Webpage': 'https://kavunnuggihalli.com/plastron/',
        'Source': 'https://github.com/kavunnuggihalli/Plastron',
    },
    python_requires='>=3.0',
    version="1.0.5",
    install_requires=[
        "setuptools",
        "art",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.0",
        "Topic :: Utilities",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.7",
        "Topic :: System :: Shells",
        "Topic :: System :: System Shells",
    ],
    include_package_data=True
)
