import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="irods-rule-wrapper",
    version="0.0.4",
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
    python_requires='>=3.6',
    install_requires=[
        'python-irodsclient @ git+https://github.com/MaastrichtUniversity/python-irodsclient.git@DHS-1146#egg=python-irodsclient'
    ],
    tests_requires=[
        'pytest'
    ],
)
