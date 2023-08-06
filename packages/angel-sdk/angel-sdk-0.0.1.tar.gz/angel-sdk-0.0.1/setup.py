from setuptools import setup, find_packages

setup(
    name="angel-sdk",
    version="0.0.1",
    author="greene",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=["requests>=2.27.1"],
)
