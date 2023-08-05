from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="basic_operations",
    version="0.0.3",
    author="Matheus Roque",
    author_email="mroque@outlook.com.br",
    description="The package is used to basic mathematics operations",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roqueds/basic_operations_package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)