import setuptools
from loguetools import version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loguetools",
    version=version.__version__,
    author="Gary Ruben",
    author_email="gary.ruben@gmail.com",
    description="Korg minilogue family patch manipulation tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'click',
        'wxPython',
    ],
    py_modules=[],
    entry_points='''
        [console_scripts]
        translate=loguetools.translate:click_translate
        explode=loguetools.explode:click_explode
        dump=loguetools.dump:click_dump
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