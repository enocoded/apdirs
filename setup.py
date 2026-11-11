from pathlib import Path

from setuptools import setup, find_packages

VERSION = Path(__file__).with_name("VERSION").read_text(encoding="utf-8").strip()

setup(
    name="apdirs",
    version=VERSION,
    packages=find_packages(),
    install_requires=[],
    author="enoforte",
    description="Archviz Project Directory Manager for Ubuntu GNOME",
    python_requires=">=3.8",
)