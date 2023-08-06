  
import setuptools
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robofloak",  # Replace with your own username
    version="0.0.1",
    author="Roboflow",
    license='GPLv3+',
    author_email="jacob@roboflow.com",
    description="python client for deploying Roboflow models to OAK devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.roboflow.com",
    install_requires=[
        "numpy==1.22.0",
        "opencv-contrib-python==4.5.5.64",
        "depthai==2.15.0.0",
        "requests==2.26.0"
    ],
    packages=find_packages(include=('robofloak',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)