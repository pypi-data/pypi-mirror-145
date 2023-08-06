# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# This call to setup() does all the work
setup(
    name="marfa_bi_connection",
    version="0.5.0",
    description="MarfaBI connections",
    url="https://github.com/NorddyM/MarfaBI",
    author="Ruslan Galimov",
    author_email="rgalimov@marfa-tech.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["marfa_bi_connection"],
    include_package_data=True,
    install_requires=['PyMySQL==1.0.2',
                      'PyYAML==6.0',
                      'sshtunnel==0.4.0',
                      'pandas==1.4.1',
                      'python-telegram-bot==13.11',
                      'SQLAlchemy==1.4.34',
                      'clickhouse-sqlalchemy==0.2.0',
                      'clickhouse-driver==0.2.3',
                      'google-cloud-bigquery==2.34.2',
                      'slack-sdk==3.15.2',
                      'google==3.0.0',
                      'cryptography==36.0.1']
)