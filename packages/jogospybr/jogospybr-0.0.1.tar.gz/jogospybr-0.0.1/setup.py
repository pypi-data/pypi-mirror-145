from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="jogospybr",
    version="0.0.1",
    author="felipeb_barreto",
    author_email="felipebbarreto22@gmail.com",
    description="Some games from Brazil in Python",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felipebbarreto/DIOgames.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.3',
    )
