from setuptools import setup, find_packages

VERSION = "0.0.3"
DESCRIPTION = "A logging package using Loki for Python"

print(find_packages())

setup(
    name="logger_bro",
    version=VERSION,
    author="Charis Giaralis",
    author_email="charis.giaralis@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["python-logging-loki", "pydantic"],
    keywords=["python", "logger"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
