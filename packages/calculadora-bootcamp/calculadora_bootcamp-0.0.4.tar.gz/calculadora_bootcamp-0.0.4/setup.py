from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="calculadora_bootcamp",
    version="0.0.4",
    author="Eduardo",
    author_email="lauer.edu@gmail.com",
    description="Criando primeiro package",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edu-lauer",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
