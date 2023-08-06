import imp
import setuptools
from pathlib import Path

setuptools.setup(
    # Set this name to a unique name that doesn't conflict with any of the other PyPi packages
    name="publishingPackages",
    version=1.0,
    # The long description should be equal to the package name
    long_description=Path(
        "PythonPackageIndex\PublishingPackages\README.md").read_text,
    # We need to tell Python to use setup_tools to find the files we wish to publish
    # We can pass directories we wish to exclude as keyword arguments to the find_package() method
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
