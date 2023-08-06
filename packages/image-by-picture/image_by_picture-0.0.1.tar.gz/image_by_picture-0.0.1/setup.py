from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_by_picture",
    version="0.0.1",
    author="Nequita",
    description="Image Processing by Picture using OpenCV and Numpy",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NEQUITA/image_by_picture",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
    setup_requires=['wheel'],
)