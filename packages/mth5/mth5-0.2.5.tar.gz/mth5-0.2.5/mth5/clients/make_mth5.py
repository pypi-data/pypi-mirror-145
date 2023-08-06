# -*- coding: utf-8 -*-
"""
Updated on Wed Aug  25 19:57:00 2021

@author: jpeacock + tronan
"""
# =============================================================================
# Imports
# =============================================================================
from pathlib import Path

import pandas as pd

from obspy.clients import fdsn
from obspy import UTCDateTime
from obspy import read as obsread
from obspy.core.inventory import Inventory

from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment

from mth5.mth5 import MTH5
from mth5.timeseries import RunTS
from mth5.helpers import validate_name

# =============================================================================


class MakeMTH5:
    def __init__(self, client="IRIS", mth5_version="0.2.0"):
        self.column_names = [
            "network",
            "station",
            "location",
            "channel",
            "start",
            "end",
        ]
        self.client = client
        self.mth5_version = mth5_version

    def _validate_dataframe(self, df):
        if not isinstance(df, pd.DataFrame):
            if isinstance(df, (str, Path)):
                fn = Path(df)
                if not fn.exists():
                    raise IOError(f"File {fn} does not exist. Check path")
                df = pd.read_csv(fn)
                df = df.fillna("")
            else:
                raise ValueError(f"Input must be a pandas.Dataframe not {type(df)}")

        if df.columns.to_list() != self.column_names:
            raise ValueError(
                f"column names in file {df.columns} are not the expected {self.column_names}"
            )

        return df

    def make_mth5_from_fdsnclient(self, df, path=None, client=None, interact=False):
        """
        Make an MTH5 file from an FDSN data center

        :param df: DataFrame with columns

            - 'network'   --> FDSN Network code
            - 'station'   --> FDSN Station code
            - 'location'  --> FDSN Location code
            - 'channel'   --> FDSN Channel code
            - 'start'     --> Start time YYYY-MM-DDThh:mm:ss
            - 'end'       --> End time YYYY-MM-DDThh:mm:ss

        :type df: :class:`pandas.DataFrame`
        :param path: Path to save MTH5 file to, defaults to None
        :type path: string or :class:`pathlib.Path`, optional
        :param client: FDSN client name, defaults to "IRIS"
        :type client: string, optional
        :raises AttributeError: If the input DataFrame is not properly
        formatted an Attribute Error will be raised.
        :raises ValueError: If the values of the DataFrame are not correct a
        ValueError will be raised.
        :return: MTH5 file name
        :rtype: :class:`pathlib.Path`


        .. seealso:: https://docs.obspy.org/packages/obspy.clients.fdsn.html#id1

        .. note:: If any of the column values are blank, then any value will
        searched for.  For example if you leave 'station' blank, any station
        within the given start and end time will be returned.



        """
        if path is None:
            path = Path().cwd()
        else:
            path = Path(path)

        if client is not None:
            self.client = client

        df = self._validate_dataframe(df)

        unique_list = self.get_unique_networks_and_stations(df)
        if self.mth5_version in ["0.1.0"]:
            if len(unique_list) != 1:
                raise AttributeError("MTH5 supports one survey/network per container.")

        file_name = path.joinpath(self.make_filename(df))

        # initiate MTH5 file
        m = MTH5(file_version=self.mth5_version)
        m.open_mth5(file_name, "w")

        # read in inventory and streams
        inv, streams = self.get_inventory_from_df(df, self.client)
        # translate obspy.core.Inventory to an mt_metadata.timeseries.Experiment
        translator = XMLInventoryMTExperiment()
        experiment = translator.xml_to_mt(inv)

        # Updates expriment information based on time extent of streams
        # rather than time extent of inventory
        # experiment = translator.drop_runs(m, streams)

        m.from_experiment(experiment)
        if self.mth5_version in ["0.1.0"]:
            for station_id in unique_list[0]["stations"]:
                # get the streams for the given station
                msstreams = streams.select(station=station_id)
                trace_start_times = sorted(
                    list(set([tr.stats.starttime.isoformat() for tr in msstreams]))
                )
                trace_end_times = sorted(
                    list(set([tr.stats.endtime.isoformat() for tr in msstreams]))
                )
                if len(trace_start_times) != len(trace_end_times):
                    raise ValueError(
                        f"Do not have the same number of start {len(trace_start_times)}"
                        f" and end times {len(trace_end_times)} from streams"
                    )
                run_list = m.get_station(station_id).groups_list

                n_times = len(trace_start_times)

                # adding logic if there are already runs filled in
                if len(run_list) == n_times:
                    for run_id, start, end in zip(
                        run_list, trace_start_times, trace_end_times
                    ):
                        # add the group first this will get the already filled in
                        # metadata to update the run_ts_obj.
                        run_group = m.stations_group.get_station(station_id).add_run(
                            run_id
                        )
                        # then get the streams an add existing metadata
                        run_stream = msstreams.slice(
                            UTCDateTime(start), UTCDateTime(end)
                        )
                        run_ts_obj = RunTS()
                        run_ts_obj.from_obspy_stream(run_stream, run_group.metadata)
                        run_group.from_runts(run_ts_obj)

                # if there is just one run
                elif len(run_list) == 1:
                    if n_times > 1:
                        for run_id, times in enumerate(
                            zip(trace_start_times, trace_end_times), 1
                        ):
                            run_group = m.stations_group.get_station(
                                station_id
                            ).add_run(f"{run_id:03}")
                            run_stream = msstreams.slice(
                                UTCDateTime(times[0]), UTCDateTime(times[1])
                            )
                            run_ts_obj = RunTS()
                            run_ts_obj.from_obspy_stream(run_stream, run_group.metadata)
                            run_group.from_runts(run_ts_obj)

                    elif n_times == 1:
                        run_group = m.stations_group.get_station(station_id).add_run(
                            run_list[0]
                        )
                        run_stream = msstreams.slice(
                            UTCDateTime(times[0]), UTCDateTime(times[1])
                        )
                        run_ts_obj = RunTS()
                        run_ts_obj.from_obspy_stream(run_stream, run_group.metadata)
                        run_group.from_runts(run_ts_obj)
                elif len(run_list) != n_times:
                    print(
                        "More or less runs have been requested by the user "
                        + "than are defined in the metadata. Runs will be "
                        + "defined but only the requested run extents contain "
                        + "time series data "
                        + "based on the users request."
                    )
                    for run_id, start, end in zip(
                        run_list, trace_start_times, trace_end_times
                    ):

                        # add the group first this will get the already filled in
                        # metadata
                        for run in run_list:
                            run_group = m.stations_group.get_station(
                                station_id
                            ).get_run(run)
                            # Chekcs for start and end times of runs
                            run_start = run_group.metadata.time_period.start
                            run_end = run_group.metadata.time_period.end
                            # Create if statment that checks for start and end
                            # times in the run.
                            # Compares start and end times of runs
                            # to start and end times of traces. Packs runs based on
                            # time spans
                            if UTCDateTime(start) >= UTCDateTime(
                                run_start
                            ) and UTCDateTime(end) <= UTCDateTime(run_end):
                                run_stream = msstreams.slice(
                                    UTCDateTime(start), UTCDateTime(end)
                                )
                                run_ts_obj = RunTS()
                                run_ts_obj.from_obspy_stream(
                                    run_stream, run_group.metadata
                                )
                                run_group.from_runts(run_ts_obj)
                            else:
                                continue
                else:
                    raise ValueError("Cannot add Run for some reason.")

        # Version 0.2.0 has the ability to store multiple surveys
        elif self.mth5_version in ["0.2.0"]:
            # mt_metadata translates the mt survey id into the survey id
            # if it is provided which will be different from the fdsn network
            # id, so we need to map the fdsn networks onto the survey id.
            survey_map = dict([(s.fdsn.network, s.id) for s in experiment.surveys])

            for survey_dict in unique_list:
                # get the mt survey id that maps to the fdsn network
                fdsn_network = survey_dict["network"]
                survey_id = survey_map[fdsn_network]

                survey_group = m.get_survey(survey_id)
                for station_id in survey_dict["stations"]:
                    # get the streams for the given station
                    msstreams = streams.select(station=station_id)
                    trace_start_times = sorted(
                        list(set([tr.stats.starttime.isoformat() for tr in msstreams]))
                    )
                    trace_end_times = sorted(
                        list(set([tr.stats.endtime.isoformat() for tr in msstreams]))
                    )
                    if len(trace_start_times) != len(trace_end_times):
                        raise ValueError(
                            f"Do not have the same number of start {len(trace_start_times)}"
                            f" and end times {len(trace_end_times)} from streams"
                        )
                    run_list = m.get_station(station_id, survey_id).groups_list
                    run_list.remove("Transfer_Functions")

                    n_times = len(trace_start_times)

                    # adding logic if there are already runs filled in
                    if len(run_list) == n_times:
                        for run_id, start, end in zip(
                            run_list, trace_start_times, trace_end_times
                        ):
                            # add the group first this will get the already filled in
                            # metadata to update the run_ts_obj.
                            run_group = survey_group.stations_group.get_station(
                                station_id
                            ).add_run(run_id)

                            # then get the streams an add existing metadata
                            run_stream = msstreams.slice(
                                UTCDateTime(start), UTCDateTime(end)
                            )
                            run_ts_obj = RunTS()
                            run_ts_obj.from_obspy_stream(run_stream, run_group.metadata)
                            run_group.from_runts(run_ts_obj)

                    # if there is just one run
                    elif len(run_list) == 1:
                        if n_times > 1:
                            for run_id, times in enumerate(
                                zip(trace_start_times, trace_end_times), 1
                            ):
                                run_group = survey_group.stations_group.get_station(
                                    station_id
                                ).add_run(f"{run_id:03}")
                                run_stream = msstreams.slice(
                                    UTCDateTime(times[0]), UTCDateTime(times[1])
                                )
                                run_ts_obj = RunTS()
                                run_ts_obj.from_obspy_stream(
                                    run_stream, run_group.metadata
                                )
                                run_group.from_runts(run_ts_obj)

                        elif n_times == 1:
                            run_group = survey_group.stations_group.get_station(
                                station_id
                            ).add_run(run_list[0])
                            run_stream = msstreams.slice(
                                UTCDateTime(times[0]), UTCDateTime(times[1])
                            )
                            run_ts_obj = RunTS()
                            run_ts_obj.from_obspy_stream(run_stream, run_group.metadata)
                            run_group.from_runts(run_ts_obj)
                    else:
                        raise ValueError("Cannot add Run for some reason.")

        if not interact:
            m.close_mth5()

            return file_name
        if interact:
            return m

    def get_inventory_from_df(self, df, client=None, data=True):
        """
        Get an :class:`obspy.Inventory` object from a
        :class:`pandas.DataFrame`

        :param df: DataFrame with columns

            - 'network'   --> FDSN Network code
            - 'station'   --> FDSN Station code
            - 'location'  --> FDSN Location code
            - 'channel'   --> FDSN Channel code
            - 'start'     --> Start time YYYY-MM-DDThh:mm:ss
            - 'end'       --> End time YYYY-MM-DDThh:mm:ss

        :type df: :class:`pandas.DataFrame`
        :param client: FDSN client
        :type client: string
        :param data: True if you want data False if you want just metadata,
        defaults to True
        :type data: boolean, optional
        :return: An inventory of metadata requested and data
        :rtype: :class:`obspy.Inventory` and :class:`obspy.Stream`

        .. seealso:: https://docs.obspy.org/packages/obspy.clients.fdsn.html#id1

        .. note:: If any of the column values are blank, then any value will
        searched for.  For example if you leave 'station' blank, any station
        within the given start and end time will be returned.

        """
        if client is not None:
            self.client = client

        df = self._validate_dataframe(df)

        # get the metadata from an obspy client
        client = fdsn.Client(self.client)

        # creat an empty stream to add to
        streams = obsread()
        streams.clear()

        inv = Inventory(networks=[], source="MTH5")

        # sort the values to be logically ordered
        df.sort_values(self.column_names[:-1])

        used_network = dict()
        used_station = dict()
        for row in df.itertuples():
            # First for loop builds out networks and stations
            if row.network not in used_network:
                net_inv = client.get_stations(
                    row.start, row.end, network=row.network, level="network"
                )
                returned_network = net_inv.networks[0]
                used_network[row.network] = [row.start]
            elif used_network.get(
                row.network
            ) is not None and row.start not in used_network.get(row.network):
                net_inv = client.get_stations(
                    row.start, row.end, network=row.network, level="network"
                )
                returned_network = net_inv.networks[0]
                used_network[row.network].append(row.start)
            else:
                continue
            for st_row in df.itertuples():
                if row.network != st_row.network:
                    continue
                else:
                    if st_row.station not in used_station:
                        sta_inv = client.get_stations(
                            st_row.start,
                            st_row.end,
                            network=row.network,
                            station=st_row.station,
                            level="station",
                        )
                        returned_sta = sta_inv.networks[0].stations[0]
                        used_station[st_row.station] = [st_row.start]
                    elif used_station.get(
                        st_row.station
                    ) is not None and st_row.start not in used_station.get(
                        st_row.station
                    ):
                        # Checks for epoch
                        sta_inv = client.get_stations(
                            st_row.start,
                            st_row.end,
                            network=st_row.network,
                            station=st_row.station,
                            level="station",
                        )
                        returned_sta = sta_inv.networks[0].stations[0]
                        used_station[st_row.station].append(st_row.start)
                    else:
                        continue
                for ch_row in df.itertuples():
                    if (
                        ch_row.network == row.network
                        and st_row.station == ch_row.station
                        and ch_row.start == st_row.start
                    ):
                        cha_inv = client.get_stations(
                            ch_row.start,
                            ch_row.end,
                            network=ch_row.network,
                            station=ch_row.station,
                            loc=ch_row.location,
                            channel=ch_row.channel,
                            level="response",
                        )
                        returned_chan = cha_inv.networks[0].stations[0].channels[0]
                        returned_sta.channels.append(returned_chan)

                        # -----------------------------
                        # get data if desired
                        if data:
                            streams = (
                                client.get_waveforms(
                                    ch_row.network,
                                    ch_row.station,
                                    ch_row.location,
                                    ch_row.channel,
                                    UTCDateTime(ch_row.start),
                                    UTCDateTime(ch_row.end),
                                )
                                + streams
                            )
                    else:
                        continue

                returned_network.stations.append(returned_sta)
            inv.networks.append(returned_network)

        return inv, streams

    def get_df_from_inventory(self, inventory):
        """
        Create an data frame from an inventory object

        :param inventory: inventory object
        :type inventory: :class:`obspy.Inventory`
        :return: dataframe in proper format
        :rtype: :class:`pandas.DataFrame`

        """

        rows = []
        for network in inventory.networks:
            for station in network.stations:
                for channel in station.channels:
                    entry = (
                        network.code,
                        station.code,
                        channel.location_code,
                        channel.code,
                        channel.start_date,
                        channel.end_date,
                    )
                    rows.append(entry)

        return pd.DataFrame(rows, columns=self.column_names)

    def get_unique_networks_and_stations(self, df):
        """
        Get unique lists of networks, stations, locations, and channels from
        a given data frame.

        [{'network': FDSN code, "stations": [list of stations for network]}]

        :param df: request data frame
        :type df: :class:`pandas.DataFrame`
        :return: list of network dictionaries with
        [{'network': FDSN code, "stations": [list of stations for network]}]
        :rtype: list

        """
        unique_list = []
        net_list = df["network"].unique()
        for network in net_list:
            network_dict = {
                "network": network,
                "stations": df[df.network == network].station.unique().tolist(),
            }
            unique_list.append(network_dict)

        return unique_list

    def make_filename(self, df):
        """
        Make a filename from a data frame that is networks and stations

        :param df: request data frame
        :type df: :class:`pandas.DataFrame`
        :return: file name as network_01+stations_network_02+stations.h5
        :rtype: string

        """

        unique_list = self.get_unique_networks_and_stations(df)

        return (
            "_".join([f"{d['network']}_{'_'.join(d['stations'])}" for d in unique_list])
            + ".h5"
        )

    def get_fdsn_channel_map(self):
        FDSN_CHANNEL_MAP = {}

        FDSN_CHANNEL_MAP["BQ2"] = "BQ1"
        FDSN_CHANNEL_MAP["BQ3"] = "BQ2"
        FDSN_CHANNEL_MAP["BQN"] = "BQ1"
        FDSN_CHANNEL_MAP["BQE"] = "BQ2"
        FDSN_CHANNEL_MAP["BQZ"] = "BQ3"
        FDSN_CHANNEL_MAP["BT1"] = "BF1"
        FDSN_CHANNEL_MAP["BT2"] = "BF2"
        FDSN_CHANNEL_MAP["BT3"] = "BF3"
        FDSN_CHANNEL_MAP["LQ2"] = "LQ1"
        FDSN_CHANNEL_MAP["LQ3"] = "LQ2"
        FDSN_CHANNEL_MAP["LT1"] = "LF1"
        FDSN_CHANNEL_MAP["LT2"] = "LF2"
        FDSN_CHANNEL_MAP["LT3"] = "LF3"
        FDSN_CHANNEL_MAP["LFE"] = "LF1"
        FDSN_CHANNEL_MAP["LFN"] = "LF2"
        FDSN_CHANNEL_MAP["LFZ"] = "LF3"
        FDSN_CHANNEL_MAP["LQE"] = "LQ1"
        FDSN_CHANNEL_MAP["LQN"] = "LQ2"
        return FDSN_CHANNEL_MAP
