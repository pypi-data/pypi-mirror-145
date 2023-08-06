#!python
"""  remap.py

A wrapper to run REMAP from within python.

Copyright 2022, Uli Wortmann, uli.wortmann@utoronto.ca

"""
from __future__ import annotations
import numpy as np
import pandas as pd


def get_delta(r: float, conc: np.array, a: int, b: int) -> float:
    """Calculate delta values from total concentration and concentration of the
    light isotope

    r = isotope standart reference ratio
    conc = nd.arrays with concentration values
    a & b = index values

    returns the delta value d
    """
    d = (
        (
            (conc[a, :] - conc[b, :]) / (conc[b, :] + (conc[b, :] == 0))
            - (r * (conc[b, :] != 0))
        )
        / r
        * 1000
    )
    return d

def run_remap(infile: pathlib.Path)-> pd.DataFrame:
    """ This function starts the octace process and rusn the
    start_remap.m script.

    infile:  A fully qualified file name of pathlib object

    The function returns:
    c: np.array of constants
    conc: np.array of concentration values
    r: ???
    v: ???
    par: np.array  of parameters
    """
    from oct2py import octave
    import pandas as pd
    import site

    # set the path where the remap_lib and start remap files live
    ip = site.getsitepackages()[0]
    octave.addpath(f"{ip}/remappy/")
    
    # call the remap solver
    [c, conc, r, v, par] = octave.start_remap(str(infile), nout=5)

    # transfer results into dataframe. Use the tolist() method to convert
    # from numpy data type
    df = pd.DataFrame()

    df["Depth"] = c.depth[0, :].tolist()
    df["Substrate"] = conc[0, :].tolist()
    df["Product"] = conc[2, :].tolist()
    df["Precipitate"] = conc[4, :].tolist()
    df["f"] = par.f[0, :].tolist()

    if c.ref != 0:
        df["Substrate d"] = get_delta(c.ref, conc, 0, 1)
        df["Product d"] = get_delta(c.ref, conc, 2, 3)
        df["Precipitate d"] = get_delta(c.ref, conc, 4, 5)
        # set all zeros to NaN, except in first row
        cols = ["Substrate d", "Product d", "Precipitate d"]
        df[cols] = df[cols][1:].replace({"0": np.nan, 0: np.nan})
    else:
        df["Substrate d"] = np.zeros(int(c.imax)) * np.nan
        df["Product d"] = np.zeros(int(c.imax)) * np.nan
        df["Precipitate d"] = np.zeros(int(c.imax)) * np.nan

    return df

if __name__ == "__main__":
    import numpy as np
    import pathlib as pl
    import sys
    import argparse
    import matplotlib.pyplot as plt
    import pandas as pd
    from remappy import plot_it

    # --------------------------- setup cmd line parsing with argparse ------------------ #
    parser = argparse.ArgumentParser(
        description="""REMAP version 0.11, Copyright (C) Boris Chernyavsky
        If you publish results which involve REMAP
        Please cite  Chernyavsky & Wortmann (2007)
        doi:10.1029/2006GC001442"""
    )
    parser.add_argument(
        "config",
        help="model configuration file, i.e. foo.rmp",
        type=str,
    )
    parser.add_argument(
        "-ns",
        "--no-save",
        help="do not save results, defaults to False",
        dest="save",
        action="store_false",
    )
    parser.add_argument(
        "-nd",
        "--no-display",
        help="do not save results, defaults to False",
        dest="display",
        action="store_false",
    )
    parser.add_argument(
        "-md",
        "--measured-data",
        help="""provide a csv file with measured data.
        This file needs to have the same format as the remap results file""",
        dest="measured_data",
        action="store",
        metavar="myfile.csv",
    )
    parser.add_argument(
        "-f",
        "--figure-name",
        dest="fig_name",
        help="figure name - defaults to 'default_fig.pdf'",
        default="default_fig.pdf",
        metavar="my_fig.pdf",
        type=str,
    )
    parser.add_argument(
        "-c",
        "--columns",
        help="""provide list of column indices to restrict which columns are
                 plotted. Note that that the first columns has an index of 0.""",
        dest="columns",
        action="store",
        metavar="0 1 4",
        default=None,
        nargs="+",
        type=int,
    )

    parser.set_defaults(feature=True)  # set defaults
    args = parser.parse_args()  # get cmd line arguments
    fn: str = args.config  # getinput file
    cwd: pl.Path = pl.Path.cwd()  # get the current working directory
    infile: pl.Path = pl.Path(f"{cwd}/{fn}")  # fully qualified file name
    outfile = infile.with_suffix(".csv")  # set the results file name

    df = run_remap(infile)  # run remap

    # --------------------------- save results as csv fie ------------------------------------ #
    if args.save:
        df.to_csv(outfile, index=False)

    # --------------------------- plot data ------------- ------------------------------------ #
    if args.display:

        if args.measured_data:
            dfn: str = args.measured_data  # getinput file
            cwd: pl.Path = pl.Path.cwd()  # get the current working directory
            datafile: pl.Path = pl.Path(f"{cwd}/{dfn}")  # fully qualified file name

            if not datafile.exists():  # check if file exist
                raise FileNotFoundError(f"Cannot find file {datafile}")

            md: pd.DataFrame = pd.read_csv(datafile)  # read data

            ax, fig = plot_it.plot_data([df, md], columns=args.columns)

        else:
            ax, fig = plot_it.plot_data(df, columns=args.columns)

        fig.tight_layout()
        plt.style.use("ggplot")
        fig.savefig(args.fig_name)
        plt.show
