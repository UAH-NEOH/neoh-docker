from pathlib import Path


def create_dirs():
    """

    :return:
    """
    # Path("/home/neoh").mkdir(parents=True, exist_ok=True)
    Path("/home/neoh-data/status").mkdir(parents=True, exist_ok=True)
    Path("/home/neoh-data/results").mkdir(parents=True, exist_ok=True)
    Path("/home/neoh-data/request").mkdir(parents=True, exist_ok=True)
    Path("/home/neoh-data/geometry").mkdir(parents=True, exist_ok=True)
    Path("/home/neoh-data/downloads").mkdir(parents=True, exist_ok=True)
