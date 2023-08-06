"""Module with functions for 'pyvueeel' subpackage."""

from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import os
import sys
from pathlib import Path
import warnings

from typing_extensions import Literal

import mylogging
from mypythontools.paths import find_path, PathLike
from mypythontools import types

# Lazy imports
if TYPE_CHECKING:
    import numpy as np
    import pandas as pd

    # import mydatapreprocessing as mdp
import pyvueeel

expose_error_callback: None | Callable[..., None] = None
json_to_py = types.json_to_py


def run_gui(
    devel: bool | None = None,
    log_file_path: PathLike | None = None,
    is_multiprocessing: bool = False,
    build_gui_path: Literal["default"] | PathLike = "default",
) -> None:
    """Function that init and run `eel` project.

    It will autosetup chrome mode (if installed chrome or chromium, open separate window with
    no url bar, no bookmarks etc...) if chrome is not installed, it open microsoft Edge (by default
    on windows).

    In devel mode, app is connected on live vue server. Serve your web application with node, debug python app
    file that calls this function (do not run, just debug - server could stay running after close and occupy
    used port). Open browser on 8080.

    Debugger should correctly stop at breakpoints if frontend run some python function.

    Note:
        Check project-starter on github for working examples and tutorial how to run.

        https://mypythontools.readthedocs.io/#project-starter

    Args:
        devel(bool | None, optional): If None, detected. Can be overwritten. Devel 0 run static assets,
            1 run Vue server on localhost. Defaults to None.
        log_file_path (PathLike | None), optional): If not exist, it will create, if exist, it will append,
            if None, log to relative log.log and only if in production mode. Defaults to None.
        is_multiprocessing (bool, optional): If using multiprocessing in some library, set up to True.
            Defaults to False.
        build_gui_path (PathLike), optional): Where the web asset is. Only if debug is 0 but not run with
            pyinstaller. If None, it's automatically find (but is slower then). If 'default', path from
            project-starter is used - 'gui/web_builded' is used. Defaults to 'default'.

    If you want to understand this technology more into detail, check this tutorial

    https://pyvueeel.readthedocs.io/tools/pyvueeel-tutorial.html
    """
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            module="EelForkExcludeFiles",
            category=ResourceWarning,
        )

    default_page = "index.html"

    if devel is None:
        # env var MY_PYTHON_VUE_ENVIRONMENT is configured and added with pyinstaller automatically
        # in build module
        devel = False if os.environ.get("MY_PYTHON_VUE_ENVIRONMENT") == "production" else True

    # Whether run is from .exe or from python
    is_built = True if getattr(sys, "frozen", False) else False

    if log_file_path:
        log_file = log_file_path
    else:
        log_file = "log.log" if is_built else None

    mylogging.config.OUTPUT = log_file  # type: ignore

    if is_built:
        # gui folder is created with pyinstaller in build
        gui_path = Path(getattr(sys, "_MEIPASS")) / "gui"
    else:
        if devel:
            gui_path = (
                find_path(
                    default_page,
                ).parents[1]
                / "src"
            )
        else:
            if build_gui_path:
                gui_path = Path(build_gui_path)

            else:
                gui_path = find_path(
                    default_page,
                    exclude_names=[
                        "public",
                        "node_modules",
                        "build",
                        "dist",
                    ],
                ).parent

    if not gui_path.exists():
        raise FileNotFoundError("Web files not found, setup `build_gui_path` (where builded index.html is).")

    if devel:

        def close_callback_function(_page, _sockets):
            """Define what happens if user closes the window.

            For devel for example it's not good to close the application.
            """

        close_callback = close_callback_function
        directory = gui_path
        app = None
        page = {"port": 8080}
        port = 8686
        init_files = [".vue", ".js", ".html"]

    else:
        close_callback = None
        directory = gui_path
        app = "chrome"
        page = default_page
        port = 0
        init_files = [".js", ".html"]

    pyvueeel.eel.init(
        directory.as_posix(),
        init_files,
        exlcude_patterns=["chunk-vendors"],
    )

    if is_multiprocessing:
        from multiprocessing import freeze_support

        freeze_support()

    mylogging.info("Py side started")

    try:

        pyvueeel.eel.start(
            page,
            mode=app,
            cmdline_args=["--disable-features=TranslateUI"],
            close_callback=close_callback,
            host="localhost",
            port=port,
            disable_cache=True,
        )

    except OSError:
        pyvueeel.eel.start(
            page,
            mode="edge",
            host="localhost",
            close_callback=close_callback,
            port=port,
            disable_cache=True,
        )

    except Exception:
        raise RuntimeError("Py side terminated...")


def expose(callback_function: Callable) -> None:
    """Wrap eel expose with try catch block and adding exception callback function.

    Used for example for printing error to the frontend.

    Args:
        callback_function (Callable): Function that will be called if exposed function fails on some error.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            module="EelForkExcludeFiles",
            category=ResourceWarning,
        )

    def inner(*args, **kwargs):
        try:
            return callback_function(*args, **kwargs)

        except Exception:  # pylint: disable=broad-except
            if callable(pyvueeel.expose_error_callback):
                pyvueeel.expose_error_callback()  # pylint: disable=not-callable
            else:
                mylogging.traceback(f"Unexpected error in function `{callback_function.__name__}`")

    pyvueeel.eel._expose(callback_function.__name__, inner)  # pylint: disable=protected-access


def to_vue_plotly(data: np.ndarray | pd.DataFrame, names: list = None) -> dict:
    """Takes data (dataframe or numpy array) and transforms it to form, that vue-plotly understand.

    Links to vue-plotly:

    https://www.npmjs.com/package/vue-plotly
    https://www.npmjs.com/package/@rleys/vue-plotly  - fork for vue 3 version

    Note:
        In js, you still need to edit the function, it's because no need to have all x axis for every column.
        Download the js function from project-starter and check for example.

    Args:
        data (np.array | pd.DataFrame): Plotted data.
        names (list, optional): If using array, you can define names. If using pandas, columns are
            automatically used. Defaults to None.

    Returns:
        dict: Data in form for plotting in frontend.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame([[1, "a"], [2, "b"]], columns=["numbers", "letters"])
        >>> to_vue_plotly(df)
        {'x_axis': [0, 1], 'y_axis': [[1, 2]], 'names': ['numbers']}
    """
    import pandas as pd
    import numpy as np

    import mydatapreprocessing as mdp

    if isinstance(data, np.ndarray):
        data = pd.DataFrame(data, columns=names)

    data = pd.DataFrame(data)

    numeric_data = data.select_dtypes(include="number").round(decimals=3)

    # TODO fix datetime
    try:
        numeric_data = mdp.misc.add_none_to_gaps(numeric_data)
    except Exception:
        pass

    numeric_data = numeric_data.where(np.isfinite(numeric_data), np.nan)

    # TODO
    # Remove dirty hack... editing lists

    values_list = numeric_data.values.T.tolist()

    for i, j in enumerate(values_list):
        values_list[i] = [k if not np.isnan(k) else None for k in j]

    # TODO use typed dict? May not work in VUE
    return {
        "x_axis": numeric_data.index.to_list(),  # type: ignore
        "y_axis": values_list,
        "names": numeric_data.columns.values.tolist(),
    }


def to_table(df: "pd.DataFrame", index: bool = False) -> dict:
    """Takes data (dataframe or numpy array) and transforms it to form, that vue-plotly library understands.

    Args:
        df (pd.DataFrame): Data.
        index (bool, optional): Whether use index as first column (or not at all).

    Returns:
        dict: Data in form for creating table in Vuetify v-data-table.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame([[1, "a"], [2, "b"]], columns=["numbers", "letters"])
        >>> to_table(df)
        {'table': [{'numbers': 1, 'letters': 'a'}, {'numbers': 2, 'letters': 'b'}], 'headers': [{'text': 'numbers', 'value': 'numbers', 'sortable': True}, {'text': 'letters', 'value': 'letters', 'sortable': True}]}
    """
    import pandas as pd
    import numpy as np

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "Only dataframe is allowed in to_table function. If you have Series, "
            "convert it to dataframe. You can use shape (1, x) for one row or use "
            "df.T and shape (x, 1) for one column."
        )

    data = df.copy()
    data = data.round(decimals=3)

    if index:
        data.reset_index(inplace=True)

    # Numpy nan cannot be send to json - replace with None
    data = data.where(~data.isin([np.nan, np.inf, -np.inf]), None)

    headers = [{"text": i, "value": i, "sortable": True} for i in data.columns]

    # TODO use typed dict
    return {
        "table": data.to_dict("records"),
        "headers": headers,
    }


# TODO
# Try to run npm run serve from app.py if not running

# try:
# if devel:

# If server is not running, it's started automatically
# import psutil
# import subprocess

# import signal
# already_run = 8080 in [i.laddr.port for i in psutil.net_connections()]

# if not already_run:

#     subprocess.Popen(f"cd '{pystore.gui_path.as_posix()}' && npm run serve", stdout=subprocess.PIPE,
#                      shell=True)
#     print("\nVue starting, reload page after loaded! \n")
#     import webbrowser
#     webbrowser.open('http://localhost:8080/', new=2)
