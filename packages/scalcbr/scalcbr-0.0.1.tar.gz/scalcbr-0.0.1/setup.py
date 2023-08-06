from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='scalcbr',
    version='0.0.1',
    author='Daniel Victor',
    # author_email='my_email',
    description='Simple Calc',
    long_description=page_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DanielVictorSR/simple_calculator_package.git',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.7',
)