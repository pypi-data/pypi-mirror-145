from setuptools import setup, find_packages

setup(
    name="magniv",
    version="0.1.17",
    py_modules=["magniv"],
    packages=find_packages(),
    install_requires=["Click", "docker"],
    entry_points={"console_scripts": ["magniv-cli = magniv.scripts.magniv:cli",],},
)
