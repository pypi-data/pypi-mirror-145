import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# The text of the DESCRIPTION file
DESCRIPTION = (HERE / "DESCRIPTION.md").read_text()

# This call to setup() does all the work
setup(
    name="drbpackagetesting",
    version="0.0.0dev1",
    description="Package Tests",
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/baxterda/packagetesting",
    author="Dawson Baxter",
    author_email="dbaxtersoftware@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests", "test", ".test", ".tests")),
    include_package_data=True,
    install_requires=[],
    python_requires='>=3.7',
    entry_points={
        "console_scripts": [
            "consoletest = drbpackagetesting.consoletest:consoletest"
        ]
    }
)

