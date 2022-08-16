from pathlib import Path
from setuptools import setup, find_packages

parent_dir = Path(__file__).resolve().parent

setup(
    name="actinia-python-client",
    # version=parent_dir.joinpath(
    #     "actinia/_version.txt").read_text(encoding="utf-8"),
    author="Anika Weinmann",
    author_email="weinmann@mundialis.de",
    description="Python client library for actinia requests.",
    long_description=parent_dir.joinpath("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/mundialis/actinia-python-client",
    license="GPLv3",
    packages=find_packages(exclude=("tests", "docs")),
    package_data={
        "": ["templates/*.json"]
    #     "": ["_version.txt"]
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=parent_dir.joinpath(
        "requirements.txt").read_text().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GPLv3 License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.8",
)
