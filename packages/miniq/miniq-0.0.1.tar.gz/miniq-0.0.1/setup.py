from ensurepip import version
from setuptools import setup, find_packages

with open("README.MD") as readme_file:
    README = readme_file.read()

setup_args = dict(
    name="miniq",
    packages=["miniq"],
    version="0.0.1",
    description="Python lib for miniQ",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Austin Chang",
    author_email="austinchang4@gmail.com",
    keywords=["miniq", "queue"],
    url="https://github.com/ac5tin/miniq-lib-python",
)

install_requires = [
    "grpcio==1.44.0",
    "protobuf==3.20.0",
]


if __name__ == "__main__":
    setup(**setup_args, install_requires=install_requires)
