# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 12:46:55 2021

@author: jpeacock
"""
import unittest
from pathlib import Path
import pandas as pd
import numpy as np

from mth5.clients.make_mth5 import MakeMTH5
from obspy.clients.fdsn.header import FDSNNoDataException
from mth5.utils.mth5_logger import setup_logger

# =============================================================================
# Test various inputs for getting metadata
# =============================================================================


class TestMakeMTH5(unittest.TestCase):
    """
    test a csv input to get metadata from IRIS

    """

    def setUp(self):

        ZUCAS04LQ1 = [
            "ZU",
            "CAS04",
            "",
            "LQE",
            "2020-06-12T18:32:17",
            "2020-07-13T19:00:00",
        ]
        ZUCAS04LQ2 = [
            "ZU",
            "CAS04",
            "",
            "LQN",
            "2020-06-12T18:32:17",
            "2020-07-13T19:00:00",
        ]
        ZUCAS04BF1 = [
            "ZU",
            "CAS04",
            "",
            "LFE",
            "2020-06-12T18:32:17",
            "2020-07-13T19:00:00",
        ]
        ZUCAS04BF2 = [
            "ZU",
            "CAS04",
            "",
            "LFN",
            "2020-06-12T18:32:17",
            "2020-07-13T19:00:00",
        ]
        ZUCAS04BF3 = [
            "ZU",
            "CAS04",
            "",
            "LFZ",
            "2020-06-12T18:32:17",
            "2020-07-13T19:00:00",
        ]
        ZUNRV08LQ1 = [
            "ZU",
            "NVR08",
            "",
            "LQE",
            "2020-06-12T18:32:17",
            "2020-07-13T19:00:00",
        ]
        ZUNRV08LQ2 = [
            "ZU",
            "NVR08",
            "",
            "LQN",
            "2020-06-12T18:32:17",
            "2020-07-13T19:00:00",
        ]
        ZUNRV08BF1 = [
            "ZU",
            "NVR08",
            "",
            "LFE",
            "2020-06-12T18:32:17",
            "2020-07-13T19:00:00",
        ]
        ZUNRV08BF2 = [
            "ZU",
            "NVR08",
            "",
            "LFN",
            "2020-06-12T18:32:17",
            "2020-07-13T19:00:00",
        ]
        ZUNRV08BF3 = [
            "ZU",
            "NVR08",
            "",
            "LFZ",
            "2020-06-12T18:32:17",
            "2020-07-13T19:00:00",
        ]
        metadata_list = [
            ZUCAS04LQ1,
            ZUCAS04LQ2,
            ZUCAS04BF1,
            ZUCAS04BF2,
            ZUCAS04BF3,
            ZUNRV08LQ1,
            ZUNRV08LQ2,
            ZUNRV08BF1,
            ZUNRV08BF2,
            ZUNRV08BF3,
        ]

        self.logger = setup_logger("test_make_mth5_v1")
        self.csv_fn = Path().cwd().joinpath("test_inventory.csv")
        self.mth5_path = Path().cwd()

        self.stations = ["CAS04", "NVR08"]
        self.channels = ["LQE", "LQN", "LFE", "LFN", "LFZ"]

        self.make_mth5 = MakeMTH5(mth5_version="0.1.0")
        self.make_mth5.client = "IRIS"
        # Turn list into dataframe
        self.metadata_df = pd.DataFrame(
            metadata_list, columns=self.make_mth5.column_names
        )
        self.metadata_df.to_csv(self.csv_fn, index=False)

        self.metadata_df_fail = pd.DataFrame(
            metadata_list, columns=["net", "sta", "loc", "chn", "startdate", "enddate"]
        )

    def test_df_input_inventory(self):
        inv, streams = self.make_mth5.get_inventory_from_df(
            self.metadata_df, data=False
        )
        with self.subTest(name="stations"):
            self.assertListEqual(
                self.stations, [ss.code for ss in inv.networks[0].stations]
            )
        with self.subTest(name="channels_CAS04"):
            self.assertListEqual(
                self.channels, [ss.code for ss in inv.networks[0].stations[0].channels]
            )
        with self.subTest(name="channels_NVR08"):
            self.assertListEqual(
                self.channels, [ss.code for ss in inv.networks[0].stations[1].channels]
            )

    def test_csv_input_inventory(self):
        inv, streams = self.make_mth5.get_inventory_from_df(self.csv_fn, data=False)
        with self.subTest(name="stations"):
            self.assertListEqual(
                self.stations, [ss.code for ss in inv.networks[0].stations]
            )
        with self.subTest(name="channels_CAS04"):
            self.assertListEqual(
                self.channels, [ss.code for ss in inv.networks[0].stations[0].channels]
            )
        with self.subTest(name="channels_NVR08"):
            self.assertListEqual(
                self.channels, [ss.code for ss in inv.networks[0].stations[1].channels]
            )

    def test_fail_csv_inventory(self):
        self.assertRaises(
            ValueError,
            self.make_mth5.get_inventory_from_df,
            *(self.metadata_df_fail, self.make_mth5.client, False),
        )

    def test_fail_wrong_input_type(self):
        self.assertRaises(
            ValueError,
            self.make_mth5.get_inventory_from_df,
            *(("bad tuple", "bad_tuple"), self.make_mth5.client, False),
        )

    def test_fail_non_existing_file(self):
        self.assertRaises(
            IOError,
            self.make_mth5.get_inventory_from_df,
            *("c:\bad\file\name", self.make_mth5.client, False),
        )

    def test_make_mth5(self):
        try:
            self.m = self.make_mth5.make_mth5_from_fdsnclient(
                self.metadata_df, self.mth5_path, interact=True
            )

            with self.subTest(name="stations"):
                self.assertListEqual(self.stations, self.m.station_list)
            with self.subTest(name="CAS04_runs"):
                self.assertListEqual(
                    ["Transfer_Functions", "a", "b", "c", "d"],
                    self.m.get_station("CAS04").groups_list,
                )
            for run in ["a", "b"]:
                for ch in ["ex", "ey", "hx", "hy", "hz"]:
                    with self.subTest(name=f"has data CAS04.{run}.{ch}"):
                        x = self.m.get_channel("CAS04", run, ch)
                        x_ts = x.to_channel_ts()
                        self.assertTrue(np.all((x_ts._ts.values == 0) == True))
            for run in ["c", "d"]:
                for ch in ["ex", "ey", "hx", "hy", "hz"]:
                    with self.subTest(name=f"has data CAS04.{run}.{ch}"):
                        x = self.m.get_channel("CAS04", run, ch)
                        x_ts = x.to_channel_ts()
                        self.assertFalse(np.all(x.hdf5_dataset == 0))
                        self.assertFalse(np.all((x_ts._ts.values == 0) == True))
            for run in ["a", "b", "c"]:
                for ch in ["ex", "ey", "hx", "hy", "hz"]:
                    with self.subTest(name=f"has data NVR08.{run}.{ch}"):
                        x = self.m.get_channel("NVR08", run, ch)
                        self.assertFalse(np.all(x.hdf5_dataset == 0))
            self.m.close_mth5()
            self.m.filename.unlink()
        except FDSNNoDataException as error:
            self.logger.warning(
                "The requested data could not be found on the FDSN IRIS server, check data availability"
            )
            self.logger.error(error)

            raise Exception(
                "The requested data could not be found on the FDSN IRIS server, check data availability"
            )

    def tearDown(self):
        self.csv_fn.unlink()


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
