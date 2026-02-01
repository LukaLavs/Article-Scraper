from setuptools import setup, find_packages

setup(
    name="store_base",
    version="0.1",
    packages=find_packages(include=["src*", "utils*"]),
)
# pip install -e .