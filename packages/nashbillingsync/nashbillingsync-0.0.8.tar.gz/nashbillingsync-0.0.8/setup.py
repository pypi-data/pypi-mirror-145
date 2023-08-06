import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nashbillingsync",
    version="0.0.8",
    author="Dansol Obondo",
    author_email="dansol@nashafrica.co",
    description='Python library for connecting to the Nash Billing Framework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://nashbillingsync.readme.io/docs",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)