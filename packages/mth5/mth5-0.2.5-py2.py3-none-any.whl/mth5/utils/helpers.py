from pathlib import Path

from mth5.mth5 import MTH5
from mth5.helpers import close_open_files


def initialize_mth5(h5_path, mode="w", file_version="0.1.0"):
    """
    mth5 initializer for the case of writting files.
    Parameters
    ----------
    h5_path : string or pathlib.Path
    mode : str
        "r": read
        "w": write
        "a": append

    Returns
    mth5.mth5.MTH5

    -------

    """
    if mode == "w":
        if h5_path:
            h5_path = Path(h5_path)
        else:
            h5_path = Path("test.h5")

        if h5_path.exists():
            print("WARN: file exists")
            close_open_files()
            h5_path.unlink()
        mth5_obj = MTH5(file_version=file_version)
        mth5_obj.open_mth5(str(h5_path), mode)

    elif mode in ["a", "r"]:
        h5_path = Path(h5_path)
        mth5_obj = MTH5(file_version=file_version)
        mth5_obj.open_mth5(h5_path, mode=mode)

    return mth5_obj


def read_back_data(mth5_path, station_id, run_id):
    """

    Parameters
    ----------
    mth5_path : string or pathlib.Path
        the full path the the mth5 that this method is going to try to read
    station_id : string
        the label for the station, e.g. "PKD"
    run_id : string
        The label for the run to read.  e.g. "001"

    Returns
    -------

    """
    processing_config = {}
    processing_config["mth5_path"] = str(mth5_path)
    processing_config["local_station_id"] = station_id
    config = processing_config
    m = initialize_mth5(config["mth5_path"], mode="r")
    local_run_obj = m.get_run(config["local_station_id"], run_id)
    local_run_ts = local_run_obj.to_runts()
    print("success")
    return local_run_obj, local_run_ts
