""" Setup file for remappy
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="remappy",  
    version="0.0.0.2",
    author="Ulrich G. Wortmann",
    license="GPL-3.0-or-later",
    author_email="uli.wortmann@utoronto.ca",
    description="Reaction-Transport Modeling in Porous Media ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uliw/remappy",
    packages=setuptools.find_packages(),
    package_data={'': ['remap_lib01.m', 'start_remap.m']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "pathlib",
        "oct2py",
    ],
)
