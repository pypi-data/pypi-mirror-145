import re
from setuptools import find_packages, setup

# Read the version and package name from cli/__init__.py
# From https://gehrcke.de/2014/02/distributing-a-python-command-line-application/
# Your setup.py should not import your package for reading the version number.
# Instead, always read it directly. In this case, I used regular expressions for extracting it.
version = re.search('^__version__\\s*=\\s*"(.*)"', open("cli/__init__.py").read(), re.M)
PACKAGE_NAME = re.search('^PACKAGE_NAME\\s*=\\s*"(.*)"', open("cli/__init__.py").read(), re.M)
if not version or not PACKAGE_NAME:
    raise Exception("Failed to parse cli/__init__.py for version and package name.")

setup(
    name=PACKAGE_NAME.group(1),
    version=version.group(1),
    # Note, we could possibly lower this but haven't yet tested older versions and haven't yet been asked to :)
    python_requires=">=3.8",
    author="Transform Data",
    author_email="marco@transformdata.io",
    description=("MetricFlow Library"),
    long_description="",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={"console_scripts": ["mf = cli.main:cli"]},
    py_modules=["main"],
    # Package details
    packages=find_packages(),
    include_package_data=True,
    # Dependencies
    setup_requires=["setupmeta"],
    install_requires=[
        "fire",
        "jinja2",
        "pandas",
        "pyyaml",
        "snowflake-sqlalchemy",
        "sqlalchemy-redshift",
        "sqlalchemy",
        "psycopg2",
        "pytest",
        "pycron",
        "jsonschema",
        "jsonformatter",
        "Werkzeug",
        "datadog",
        "ddtrace",
        "requests",
        "readerwriterlock",
        "graphene",
        "mysqlclient",
        "moz-sql-parser",
        "pytest-xdist",
        "snowflake-connector-python",
        "tabulate",
        "pydantic",
    ],
)
