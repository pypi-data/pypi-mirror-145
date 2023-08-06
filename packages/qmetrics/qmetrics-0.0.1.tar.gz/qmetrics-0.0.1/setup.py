import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qmetrics",
    version="0.0.1",
    author="Rajesh Sathya Kumar",
    author_email="rsathyak@asu.edu",
    description="Performance Metrics for Quantum Simulators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src", exclude=["examples", "__data", "__images"]),
    install_requires=[
          'matplotlib',
    ],
    python_requires=">=3.6",
)