from setuptools import find_packages, setup

with open("README.md", "r") as rm:
    long_description = rm.read()

version = "0.1.13"

setup(
    name="phidata",
    version=version,
    author="Ashpreet Bedi",
    author_email="ashpreet@phidata.com",
    description="Build data products as code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.phidata.com",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "docker",
        "kubernetes",
        f"phicli=={version}",
        "pydantic",
        "pyyaml",
        "rich",
        "types-PyYAML",
        "typing-extensions",
    ],
    python_requires=">=3.7",
)
