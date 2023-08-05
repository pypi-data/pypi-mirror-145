from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="package-processing-image",
    version="0.0.2",
    author="Marlon_Martins",
    description="Estudos de pacotes - Image Processing ",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/snitraMnolraM/package-processing-Image",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)