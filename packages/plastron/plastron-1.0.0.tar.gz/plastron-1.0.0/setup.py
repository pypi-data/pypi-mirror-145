import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="plastron",
    version="1.0.0",
    description="An interactive shell library",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kavunnuggihalli/Plastron",
    author="Kavun Nuggihalli",
    author_email="kavunnuggihalli@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["plastron"],
    include_package_data=True,
    install_requires=["art"],
)
