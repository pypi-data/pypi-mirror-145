from setuptools import setup

setup(
    name = "weird_json",
    version = "0.1.0",
    author = "weerdy15",
    author_email = "igorekkrupskij@gmail.com",
    description = "My implementation for JavaScript Object Notation",
    long_description = 'Behaviour the same as the JavaScript\'s global `JSON` object.\'WARNING: Array (list) decoding is not currently supported, and any JSON containing arrays will fail!',
    long_description_content_type="text/markdown",
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = ['weird_json'],
    project_urls = {
        "Bug Tracker": "https://github.com/weerdy15/weird_json/issues"
    },
    python_requires = ">=3.7",
)