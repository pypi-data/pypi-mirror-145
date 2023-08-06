import pathlib as pl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_data(plot_data, **kwargs) -> list:
    """plot_data = dataframe object or file name (or list). Both need
    to list the column header in row 1, and depth in column 1

    Optional arguments:

    fig = optional canvas handle, otherwise figure will be created
    ax = see fig
    columns = optional list, otherwise plot all columns of df
    xlabels = optional list of strings
    ylabel = optional, defaults to Depth [mbsf]

    returns the figure and graph handles

    """

    # provide defaults if none given
    defaults = {
        "fig": None,
        "ax": None,
        "columns": None,
        "xlabels": None,
        "ylabel": "Depth [mbsf]",
    }

    # check optional arguments
    dc = defaults.copy()
    for k, v in dc.items():
        if k in kwargs:
            defaults[k] = kwargs[k]

    # check for invalid keywords
    for k, v in kwargs.items():
        if k not in defaults:
            raise ValueError(f"{k} is an invalid keywords")

    # make sure we have a list
    if not isinstance(plot_data, list):
        plot_data = [plot_data]

    if defaults["fig"]:
        fig = defaults["fig"]
    else:
        fig = None

    xlabels = defaults["xlabels"]

    # loop over list elements
    j = 0
    for df in plot_data:
        # test what data we have
        if isinstance(df, str):
            cwd: pl.Path = pl.Path.cwd()  # get the current working directory
            fqfn: pl.Path = pl.Path(f"{cwd}/{df}")  # fully qualified file name

            if not fqfn.exists():  # check if file exist
                raise FileNotFoundError(f"Cannot find file {fqfn}")

            df = pd.read_csv(fqfn)

        elif not isinstance(df, pd.DataFrame):
            raise ValueError("df must be filename object or dataframe")

        # get number of columns in dataframe
        headers: list = list(df.columns)

        # check if we only print a selection
        if defaults["columns"]:
            cols = defaults["columns"]
        else:
            cols = range(len(headers) - 1)

        # set line color
        color = f"C{j}"
        # create figure object if necessary
        if not fig:
            fig, ax = plt.subplots(1, len(cols))
            fig.set_size_inches(3 * len(cols), 6)

        # loop over data (ignore depth column)
        depth = df.iloc[:, 0]
        i = 0
        u = 0
        for o in headers[1:]:
            if i in cols:
                if j == 0:
                    ax[u].plot(df[o], depth, color=color, label=o)
                else:
                    ax[u].scatter(df[o], depth, color=color, label=o)
                    
                if xlabels:
                    ax[u].set_xlabel(xlabels[i])
                else:
                    ax[u].set_xlabel(f"{o}")
                if j == 0:
                    ax[u].invert_yaxis()
                ax[u].legend()
                u = u + 1
            i = i + 1
        j = j + 1
    ax[0].set_ylabel(defaults["ylabel"])
    return [ax, fig]


# what do to when used as stand alone program
if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="""plot_it.py: plots remap stytle output data.
                                   I.e., the first column must contain depths data,
                                   and all other columns must contain data that
                                   varies with depth.

    The first row must contain headers. NaN and missing data may not be handled
    gracefully. Data must be in csv format
    """
    )
    parser.add_argument(
        "data_filename",
        help="one or more filenames with data in csv format",
        nargs="+",
        type=str,
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
        metavar="[0, 1, 4]",
        default=None,
        nargs="+",
        type=int,
    )
    

    args = parser.parse_args()  # get cmd line arguments

    ax, fig = plot_data(args.data_filename, columns=args.columns)
    fig.tight_layout()
    plt.style.use("ggplot")
    plt.show
    fig.savefig(args.fig_name)
