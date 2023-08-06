import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="Random String Maker",
    version="2.0",
    author="Aidan Hetherington",
    description="A simple random string generator I built in my free time.",
    long_description=long_description,
    packages=["randomstring"],
    license="MIT"
)