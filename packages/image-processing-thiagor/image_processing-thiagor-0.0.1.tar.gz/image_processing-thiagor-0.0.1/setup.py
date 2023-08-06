from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing-thiagor",
    version="0.0.1",
    author="Thiago Regis",
    author_email="thigorn@gmail.com",
    description="Projeto realizado através do bootcamp da DIO, Desenvolvedora Karina Kato",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thiagoregis1/image-processing-thiagor",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)