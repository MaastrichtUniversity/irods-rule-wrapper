import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="irods-rule-wrapper",
    version="1.0.0",
    author="DataHub",
    author_email="author@example.com",
    description="This repository contains the python code with the irods rule logic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MaastrichtUniversity/irods-rule-wrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "python-irodsclient==1.1.6",
        "cedar-parsing-utils @ git+https://github.com/MaastrichtUniversity/cedar-parsing-utils.git@v1.0.0#egg=cedar-parsing-utils",
        "dh-python-irods-utils @ git+https://github.com/MaastrichtUniversity/dh-python-irods-utils.git@v1.2.4#egg=dh-python-irods-utils",
        "pytz>=2021.3",
        "pydantic>=1.9.1,<2.0.0",
    ],
    tests_requires=["pytest"],
)
