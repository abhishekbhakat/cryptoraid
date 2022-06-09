from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

def find_install_requires():
    with open("requirements.txt", "r") as fh:
        requirements = [x.strip() for x in
                        fh.read().splitlines()
                        if x.strip() and not x.startswith('#')]
    return requirements

setup(
    name='cryptoraid',
    version='0.2.0',
    description='Auto crypto trader',
    author='Abhishek Bhakat',
    author_email='abhishek.bhakat@hotmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=find_install_requires(),
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.7',
)