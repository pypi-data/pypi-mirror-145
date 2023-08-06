from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='spds',
    version='0.0.0-alpha',
    author="Abhishek Mamgain",
    description="Open sourse software for pipeline design",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                     # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    # py_modules=["spds"],             # Name of the python package
    # package_dir={'':'spds'},     # Directory of the source code of the package
    install_requires=[]                     # Install other dependencies if any
)