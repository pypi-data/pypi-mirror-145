import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

version_path = HERE / "incase" / "__version__.py"
with open(version_path, "r") as fh:
    version_dict = {}
    exec(fh.read(), version_dict)
    VERSION = version_dict["__version__"]

setup(
    name="incase",
    version=VERSION,
    author="Patrick Shechet",
    author_email="patrick.shechet@gmail.com",
    description=(""),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kajuberdut/incase",
    license=None,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    entry_points={
        "console_scripts": [
            "incase=incase:cli",
        ]
    },
)
