"""Setup codes for the ALIS Python Package"""

from os.path import dirname, realpath
from setuptools import find_packages, setup


MIN_REQS = [
    'numpy>=1.21.2'
    'scipy>=1.7.3'
    'scikit-learn>=1.0.2'
    'dask[complete]>=2021.10.0'
    'matplotlib>=3.5.1'
    'networkx>=2.6.2'
    'ipywidgets>=7.7.0'
    'graphframes>=0.6'
    'kafka-python>=2.0.2'
    'pyspark==3.1.2'
    'seaborn>=0.11.2'
]

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
        install_requires=MIN_REQS,
    )
