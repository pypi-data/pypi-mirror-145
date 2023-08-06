import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="chatanalytics",
    version="0.0.7",
    description="Twitch Chat Analytics Bot",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/baxterda/chatanalytics",
    author="Dawson Baxter",
    author_email="dbaxtersoftware@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    # packages = ['chatanalytics'],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "chatter = chatanalytics.__main__:testing",
        ]
    },
)