import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loguetools",
    version="0.1.0",
    author="Gary Ruben",
    author_email="gary.ruben@gmail.com",
    description="Korg minilogue family patch manipulation tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'Click',
    ],
    py_modules=[],
    entry_points='''
        [console_scripts]
        translate=loguetools.translate:translate
        explode=loguetools.explode:explode
        dump=loguetools.dump:dump
    ''',
    url="https://github.com/gazzar/loguetools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)