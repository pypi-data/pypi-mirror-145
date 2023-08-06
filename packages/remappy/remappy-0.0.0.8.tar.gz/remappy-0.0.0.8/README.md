## Overview

REMAP (Chernyavsky & Wortmann, 2007, DOI 10.1029/2006GC001442) provides an easy to use interface for 1-dimensional reaction-transport modeling in porous media, and provides explicit support for kinetic stable isotope fractionation calculations.

The original program was written as matlab program. Remappy provides a python wrapper to the original code which can be run via `oct2py`.


## News:

-   April 6<sup>th</sup>: v 0.0.0.8 build process now uses setuptools which should automatically create an executable remap.py script.
-   April 5<sup>th</sup>: v 0.0.0.4, installation path is now updated during installation, non-python files are now included in installation script. Updated installation instructions
-   March 30<sup>th</sup>: Initial release


## Installation

-   `python -m pip install remappy` will install all necessary files and dependencies
-   you can now import remap into your python code (see below)
-   The install process should have created a standalone remap.py script which you can run from the command line. Try `remap.py --help`. This works for linux, and should work for Mac and Windows as well. If it fails you need to follow your os specific instructions on how to create an executable python program. On linux, it is sufficient to link `remap.py` to a directory which is in your path (often `/usr/local/bin/`) and set is a executable. Tools like <https://datatofish.com/executable-pyinstaller/> will also work on Mac and Windows.


## Usage

-   remap.py: This behaves similar to the original remap but provides extended command-line parsing options, run `remap.py --help` for details
-   you can also import the library and use it inside of your own python code. The remap data will be returned as pandas dataframe.

```python
import remap
import pathlib as pl
import pandas as pd

fn: str = "hg.rmp"  # remap config file
cwd: pl.Path = pl.Path.cwd()  # get the current working directory
fqfn: pl.Path = pl.Path(f"{cwd}/{fn}")  # fully qualified file name

if not fqfn.exists():  # check if file exist
    raise FileNotFoundError(f"Cannot find file {fn}")

# run remap and return results as dataframe
df: pd.DataFrame = remap.run_remap(str(fname))
```

-   or use the `oct2py` interface directly

```python
from oct2py import octave

octave.addpath("/path/to/remap.m")

fn = "hg.rmp"  # name of remap configuration file
# call remap
[c, conc, r, v, par] = octave.start_remap(fn, nout=5)
```


# Documentation

See the `pdf-docs` folder for the original REMAP documentation (see, e.g. <https://github.com/uliw/remappy>)


# Todo

-   port more matlab code to python
-   provide more examples
-   do more testing


# License

remappy: reaction-transport modeling Copyright (C), 2022 Ulrich G. Wortmann

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.