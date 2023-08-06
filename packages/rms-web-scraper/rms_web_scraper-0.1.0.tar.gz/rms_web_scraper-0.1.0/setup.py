import re
from pathlib import Path

from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    version = Path(package, "__version__.py").read_text()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", version).group(1)


def get_long_description():
    """
    Return the README.
    """
    long_description = ""
    with open("README.md", encoding="utf8") as f:
        long_description += f.read()
    long_description += "\n\n"
    with open("CHANGELOG.md", encoding="utf8") as f:
        long_description += f.read()
    return long_description


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [str(path.parent) for path in Path(package).glob("**/__init__.py")]

def get_requirements():
    """
    Return list of requirements
    """
    with open("requirements.txt", encoding="utf-8") as f:
        requirements = f.read()
    return requirements.splitlines()


setup(
    name="rms_web_scraper",
    python_requires=">=3.6",
    version=get_version("rms_web_scraper"),
    url="https://github.com/newvicx/rms_web_scraper",
    project_urls={
        "Changelog": "https://github.com/newvicx/rms_web_scraper/blob/master/CHANGELOG.md",
        "Source": "https://github.com/newvicx/rms_web_scraper",
    },
    license="MIT",
    description="Access DASH RMS data",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Chris Newville",
    author_email="chrisnewville1396@gmail.com",
    package_data={"rms_web_scraper": ["py.typed"]},
    packages=get_packages("rms_web_scraper"),
    include_package_data=True,
    zip_safe=False,
    install_requires=get_requirements(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Internet :: WWW/HTTP",
        "Framework :: AsyncIO",
        "Programming Language :: Python :: 3",
    ],
)