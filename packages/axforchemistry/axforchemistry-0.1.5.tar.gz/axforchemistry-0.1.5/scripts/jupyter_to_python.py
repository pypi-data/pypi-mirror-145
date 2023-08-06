"""Convert Jupyter notebook tutorials to Python scripts."""
from glob import glob
from os import path
from pathlib import Path
from nbformat import reads, NO_CONVERT
from nbconvert import PythonExporter


def convertNotebookInplace(notebookPath):
    """Convert Jupyter Notebook to Python file.

    Modified from https://stackoverflow.com/a/38248141/13697228

    Parameters
    ----------
    notebookPath : str
        Path to .ipynb file
    modulePath : str
        path to .py file
    """
    with open(notebookPath) as fh:
        nb = reads(fh.read(), NO_CONVERT)

    exporter = PythonExporter()
    source, _ = exporter.from_notebook_node(nb)

    py_path = str(Path(fpath).with_suffix("")) + ".py"

    with open(py_path, "w+") as fh:
        fh.writelines(source)


tutorial_dir = "tutorials"
fpaths = glob(path.join(tutorial_dir, "*.ipynb"))
for fpath in fpaths:
    convertNotebookInplace(fpath)
