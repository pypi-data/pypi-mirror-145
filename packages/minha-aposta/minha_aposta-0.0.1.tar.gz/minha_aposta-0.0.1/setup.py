from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="minha_aposta",
    version="0.0.1",
    author="netotricca",
    author_email="netotricca@gmail.com",
    description="Meu pacote de apostas",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NetoTricca/minha_aposta_package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
