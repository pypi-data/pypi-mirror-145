"""Setup codes for the ALIS Python Package"""

from os.path import dirname, realpath
from setuptools import find_packages, setup


def _read_requirements_file():
    """Return packages found in the requirements.txt"""
    file_path = "%s/requirements.txt" % dirname(realpath(__file__))
    with open(file_path) as f:
        return [line.strip() for line in f]


# Get version from __init__.py at root
with open("alis/__init__.py") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.strip().split()[-1][1:-1]

if __name__ == "__main__":

    setup(
        name='python-alis',
        version=version,
        maintainer="AIM PhDinDS 2024",
        maintainer_email="llorenzo@aim.edu",
        author="AIM PhDinDS 2024",
        author_email="llorenzo@aim.edu",
        description="A collection of algorithms for scalable data science",
        keywords=["scalable", "data science", "networks", "hash functions"],
        packages=find_packages(),
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        url="https://github.com/phdinds-aim/alis",
        install_requires=_read_requirements_file(),
    )
