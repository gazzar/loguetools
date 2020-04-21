import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    version="0.0.1",
    author="Gary Ruben",
    author_email="gary.ruben@gmail.com",
    description="Korg minilogue family patch manipulation tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gazzar/loguetools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)