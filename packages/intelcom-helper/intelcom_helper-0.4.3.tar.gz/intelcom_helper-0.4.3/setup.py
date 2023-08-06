import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="intelcom_helper",
    version="0.4.3",  # Update this for every new version
    author="Simon Prudhomme",
    author_email="sphomme@intelcomexpress.com",
    description="Code used frequently at Intelcom",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pandas',
                      'snowflake-connector-python[pandas]',
                      'snowflake-sqlalchemy',
                      'sqlalchemy'],
    url="",
    packages=setuptools.find_packages(),
    classifiers=(  # Classifiers help people find your
        "Programming Language :: Python :: 3",  # projects. See all possible classifiers
        "License :: OSI Approved :: MIT License",  # in https://pypi.org/classifiers/
    ),
)
