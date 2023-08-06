from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

DESCRIPTION = 'A tiny package that helps you validate Saudi national or iqama ids'
LONG_DESCRIPTION = (here / "README.md").read_text(encoding="utf-8")

setup(
    # the name must match the folder name 'verysimplemodule'
    name="saudi-ids-validator",
    version="0.0.1",
    author="Mohammed Alzaid",
    author_email="m7md.alzaid5@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/malzaid0/saudi-id-validator-pypi/",
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=["saudi", "saudi national", "iqama", "saudi id", "saudi arabia", "saudi id validator"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    project_urls={
        "Bug Reports": "https://github.com/malzaid0/saudi-id-validator-pypi/issues",
        "Source": "https://github.com/malzaid0/saudi-id-validator-pypi/",
    },
)
