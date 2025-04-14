from setuptools import setup, find_packages

setup(
    name="clickup-python-sdk",
    version="1.0.0",  # Match VERSION in config.py
    description="Python SDK for the ClickUp API",
    long_description=open("README.txt").read(),
    author="Michael",
    author_email="michaelbroyles68@gmail.com",
    url="https://github.com/yourusername/clickup-python-sdk",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3",
        "certifi>=2025.1.31",
        "charset-normalizer>=3.4.1",
        "idna>=3.10",
        "urllib3>=2.4.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
)
