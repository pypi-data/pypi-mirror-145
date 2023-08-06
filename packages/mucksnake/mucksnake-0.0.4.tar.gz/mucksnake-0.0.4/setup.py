"""Setup configuration and dependencies for pystonkslib."""

from os import path

from setuptools import find_packages, setup

with open("requirements.txt") as req_file:
    REQUIREMENTS = req_file.readlines()


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

COMMANDS = [
    "mucksnake=mucksnake.snake:main",
]

setup(
    name="mucksnake",
    version="0.0.4",
    author="Aaron Muckleroy",
    author_email="bubthegreat@gmail.com",
    url="https://gitlab.com/bubthegreat/mucksnake",
    include_package_data=True,
    description="This is a snake game made by a friend who passed away.  He made this game to make others happy -  he will be remembered and missed",
    long_description=LONG_DESCRIPTION,
    packages=find_packages("src"),
    package_dir={"": "src",},
    python_requires=">=3.6.6",
    entry_points={"console_scripts": COMMANDS},
    install_requires=REQUIREMENTS,
)
