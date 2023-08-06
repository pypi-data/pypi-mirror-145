from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Dio-Images",
    version="0.0.1",
    author="theoldwine",
    author_email="sior@outlook.com",
    description="projeto python leitura da imagem",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Theoldwine/package-template",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)