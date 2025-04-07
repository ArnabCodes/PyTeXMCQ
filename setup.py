"""
Setup configuration for PyTeXMCQ.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pytexmcq",
    version="1.0.0",
    author="Arnab Acharya",
    author_email="your.email@example.com",
    description="A LaTeX-based Multiple Choice Question Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArnabCodes/PyTeXMCQ",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Education :: Testing",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyPDF2>=3.0.0",
    ],
    package_data={
        'pytexmcq': ['templates/*.tex'],
    },
    entry_points={
        'console_scripts': [
            'pytexmcq=pytexmcq.__main__:main',
        ],
    },
) 