from gettext import install
from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    page_description = f.read()

with open('requirements.txt', 'r') as f:
    page_description = f.read()


setup(
    name = 'Projeto_ETL',
    version='0.0.1',
    author='Cesar Szabo',
    description='Extração e tratamento de dados via Python',
    long_description=page_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
   )
