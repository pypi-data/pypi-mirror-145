"""Convert Jupyter notebook tutorials to Python scripts."""
from glob import glob
from os import path
from pathlib import Path
from jupytext import read, write


def convertScriptInplace(scriptPath):
    """Convert Jupyter Notebook to Python file.

    Modified from https://stackoverflow.com/a/38248141/13697228

    Parameters
    ----------
    scriptPath : str
        Path to .py file
    """
    nb = read(scriptPath)
    notebook_path = str(Path(fpath).with_suffix("")) + ".ipynb"
    write(nb, notebook_path)


tutorial_dir = "tutorials"
fpaths = glob(path.join(tutorial_dir, "*.py"))
for fpath in fpaths:
    convertScriptInplace(fpath)
