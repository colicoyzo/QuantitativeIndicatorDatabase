"""
Setup script for quant_indicator_db package
"""

from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="quant-indicator-db",
    version="0.1.0",
    author="Quant Team",
    author_email="quant@example.com",
    description="A Python library for calculating, storing, and analyzing quantitative financial indicators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/quant-indicator-db",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
        "pandas>=1.2.0",
        "sqlalchemy>=1.4.0",
        "flask>=2.0.0",
        "futu-api>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
        ],
    },
)