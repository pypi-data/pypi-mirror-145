from setuptools import find_packages, setup

with open("README.md", "r") as rm:
    long_description = rm.read()

version = "0.1.13"

setup(
    name="phicli",
    version=version,
    author="Ashpreet Bedi",
    author_email="ashpreet@phidata.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.phidata.com",
    packages=find_packages(),
    install_requires=[
        "click==8.0.4",
        "boto3",
        "docker",
        "gitpython",
        "httpx",
        "kubernetes",
        "pydantic",
        "pyyaml",
        "rich",
        "typer",
        "types-PyYAML",
        "typing-extensions",
    ],
    python_requires=">=3.7",
    entry_points={"console_scripts": ["phi=phi.cli.cli_app:cli_app"]},
)
