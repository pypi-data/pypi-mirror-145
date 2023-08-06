from setuptools import setup, find_packages
from pathlib import Path

VERSION = "1.0.0"
DESCRIPTION = "The module of the program \"Predictioner\""
path = Path(__name__).parent
long_description = (path / "README.md").read_text()

# Setting up
setup(
    name="predictioner",
    version=VERSION,
    author="Marco Vidali",
    author_email="<vidali.marco@protonmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["tabulate", "tensorflow", "numpy", "matplotlib"],
    keywords=["prediction", "predictioner", "sequence", "math", "algebra", "geometry", "arithmetic", "neural networks", "ai", "artificial intelligence"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
