import os

from pathlib import Path
from os import environ


def clear_multiproc_dir():
    """
    This function will clear all files in PROMETHEUS_MULTIPROC_DIR

    This function need to be call everytime before execute service that use multiprocess(have multiple workers)
    """
    MULTIPROC_DIR = environ.get("PROMETHEUS_MULTIPROC_DIR")
    if MULTIPROC_DIR:
        file_path = Path(MULTIPROC_DIR)
        if os.path.isdir(file_path):
            for f in os.listdir(file_path):
                os.remove(os.path.join(file_path, f))
        else:
            os.mkdir(file_path)
