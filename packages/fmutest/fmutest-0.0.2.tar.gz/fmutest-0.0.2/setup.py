import setuptools


setuptools.setup(
    name="fmutest",
    version="0.0.2",
    author="Konstantin Filonenko/DTU Compute",
    author_email="kofi@dtu.dk",
    description="Library for testing of energy FMUs, repository: https://lab.compute.dtu.dk/kofi/fmutest",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8',
)