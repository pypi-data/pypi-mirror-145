from setuptools import setup
from pathlib import Path

path = Path(__file__).parent
README = (path / "README.md").read_text()

setup(
    name='terminalpyth',
    author='Cargo',
    license='MIT',
    long_description=README,
    long_description_type='text/markdown',
    license_files='LICENSE.txt',
    description='Terminal extension for python',
    version='2.0.0',
    packages=['terminalpy']
)