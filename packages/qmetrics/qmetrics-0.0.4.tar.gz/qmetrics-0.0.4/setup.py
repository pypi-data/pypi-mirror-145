import os

from setuptools import setup, find_packages

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'README.md')
with open(README_PATH) as readme_file:
    README = readme_file.read()

requirements = [
    "matplotlib"
]

setup(
    name="qmetrics",
    version="0.0.4",
    description="Quantum Performance Metrics",
    long_description=README,
    long_description_content_type='text/markdown',
    url="https://github.com/rsathyak/qml_masters_thesis/tree/main/experiments/qmetrics",
    author="Rajesh",
    author_email="rsathyak@asu.edu",
    license="Apache 2.0",
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
    ],
    keywords="quantum performance volume",
    install_requires=requirements,
    project_urls={
        "Bug Tracker": "https://github.com/rsathyak/qml_masters_thesis/issues",
        "Documentation": "https://github.com/rsathyak/qml_masters_thesis/tree/main/experiments/qmetrics/README.MD",
        "Source Code": "https://github.com/rsathyak/qml_masters_thesis/tree/main/experiments/qmetrics",
    },
    include_package_data=True,
    python_requires=">=3.7",
    packages=find_packages(),
)