from flake8_docstring_checker import __version__
from setuptools import setup


with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()


setup(
    name="flake8-docstring-checker",
    version=__version__,
    py_modules=["flake8_docstring_checker"],
    description="A simple flake8 plugin that checks if everything has a docstring",
    long_description=description,
    long_description_content_type="text/markdown",
    author="JakobDev",
    author_email="jakobdev@gmx.de",
    url="https://gitlab.com/JakobDev/flake8-docstring-checker",
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=["flake8"],
    license="BSD",
    keywords=["JakobDev", "Docstrings", "flake8"],
    entry_points={
        "flake8.extension": [
            'DC = flake8_docstring_checker:Plugin',
        ],
    },
    project_urls={
        "Bug Tracker": "https://gitlab.com/JakobDev/flake8-docstring-checker/-/issues"
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Environment :: Other Environment",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ]
)
