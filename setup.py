import setuptools

with open("README.md", "r") as d:
    long_description = d.read()

requirements = []
with open("requirements.txt") as r:
    requirements = r.read().splitlines()

setuptools.setup(
    name="pryncess",
    version="1.0.0",
    author="EthanSk13s",
    description="A Python REST API wrapper for Princess",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EthanSk13s/pryncess",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ),
)