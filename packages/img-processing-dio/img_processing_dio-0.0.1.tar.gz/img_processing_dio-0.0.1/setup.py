from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="img_processing_dio",
    version="0.0.1",
    author="Thiago Souza",
    author_email="thiagolsmail@gmail.com",
    description="Projeto DIO",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thiagosouzalink/cricao-pacote-processamento-image-dio.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)