## Overview

REMAP (Chernyavsky & Wortmann, 2007) provides an easy to use interface for 1-dimensional reaction-transport modeling in porous media, and provides explicit support for kinetic stable isotope fractionation calculations.

The original program was written as matlab program. Remappy provides a python wrapper to the original code which can be run via `oct2py`.


## News:

-   March 30<sup>th</sup>: Initial release


## Usage

-   remap.py: This behaves similar to the original remap but provides extended command-line parsing options, run `remap.py --help` for details
-   you can also import the library and use it inside of your own python code

```ipython
import remap
import pathlib as pl
import pandas as pd

fn: str = "hg.rmp"  # remap config file
cwd: pl.Path = pl.Path.cwd()  # get the current working directory
fqfn: pl.Path = pl.Path(f"{cwd}/{fn}")  # fully qualified file name

if not fqfn.exists():  # check if file exist
    raise FileNotFoundError(f"Cannot find file {fn}")
df: pd.DataFrame = remap.run_remap(str(fname))
```

-   or use the `oct2py` interface directly

```ipython
from oct2py import octave

octave.addpath("/path/to/remap.m")

fn = "hg.rmp"  # name of remap configuration file
# call remap
[c, conc, r, v, par] = octave.start_remap(fn, nout=5)
```


## Installation

-   `pip install remmapy` will install all necessary files and dependencies
-   Afterwards you need to find `remap.py` and change the following line:

```ipython
octave.addpath("/path/to/remap.m")
```

so that it points to the location of the octave matlab file.


# Documentation

See the `docs` folder for the original REMAP documentation.


# Todo

-   port more matlab code to python
-   provide more examples
-   do more testing


# License

remappy: reaction-transport modeling Copyright (C), 2022 Ulrich G. Wortmann

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.