from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='EventsPP',
    version='0.0.3',
    description='A package for event-driven paradigm',
    packages=find_packages(),
    url='https://github.com/Mateus-SF/EventsPP',
    author='Mateus Ferreira',
    author_email='mateus03ferreira04@gmail.com',
    license='MIT',
    zip_safe=False,
    long_description=(Path(__file__).parent/'README.md').read_text(),
    long_description_content_type='text/markdown'
)
