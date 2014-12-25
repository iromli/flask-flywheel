"""
Flask-Flywheel
--------------

Adds Flywheel support to your Flask application.
"""
import re
from setuptools import setup


# Get version without importing, which avoids dependency issues
def get_version():
    with open("flask_flywheel/_meta.py") as f:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         f.read()).group('version')


setup(
    name="flask-flywheel",
    version=get_version(),
    url="http://github.com/iromli/flask-flywheel",
    license="MIT",
    author="Isman Firmansyah",
    author_email="isman.firmansyah@gmail.com",
    description="Adds Flywheel support to your Flask application",
    long_description=__doc__,
    packages=["flask_flywheel"],
    zip_safe=False,
    install_requires=[
        "flywheel",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
    ]
)
