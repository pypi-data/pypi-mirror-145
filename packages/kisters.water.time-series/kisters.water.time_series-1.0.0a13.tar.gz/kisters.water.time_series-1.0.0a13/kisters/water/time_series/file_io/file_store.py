import asyncio
import logging
import os
import re
from datetime import datetime
from typing import Any, Iterable, List, Mapping, Optional, Union

import pandas as pd

from kisters.water.time_series.core import TimeSeriesTransaction
from kisters.water.time_series.core.time_series import TimeSeries, TimeSeriesColumnT
from kisters.water.time_series.core.time_series_store import TimeSeriesStore, make_iterable
from kisters.water.time_series.file_io.file_time_series import FileEnsembleTimeSeries, FileTimeSeries
from kisters.water.time_series.file_io.time_series_format import TimeSeriesFormat

logger = logging.getLogger(__name__)


class FileStore(TimeSeriesStore):
    """FileStore provides a TimeSeriesStore for your local time series data files

    Args:
        root_dir: The path to your time series data folder.
        file_format: The format used by your time series data files.

    Examples:
        .. code-block:: python

            from kisters.water.time_series.file_io import FileStore, ZRXPFormat
            fs = FileStore('tests/data', ZRXPFormat())
            ts = fs.get_by_path('validation/inner_consistency1/station1/H')
    """

    def __init__(self, root_dir: str, file_format: TimeSeriesFormat):
        file_format._TimeSeriesFormat__root_dir = root_dir
        self.__file_format = file_format
        self.__root_dir = root_dir
        if not os.path.isdir(self.__root_dir):
            raise FileNotFoundError("Path " + os.path.abspath(self.__root_dir) + " does not exist")

    def create_time_series(
        self, path: str, metadata: dict = None, columns: List[TimeSeriesColumnT] = None, **kwargs
    ) -> TimeSeries:
        if metadata is None:
            metadata = {}
        self.__file_format.writer.write(
            file=os.path.join(self.__root_dir, path + "." + list(self.__file_format.extensions)[0]),
            data_list=[pd.DataFrame()],
            meta_list=[{"name": metadata.get("name"), **metadata}],
        )
        return self.get_by_path(path)

    def create_time_series_from(self, copy_from: TimeSeries, new_path: str = None) -> TimeSeries:
        meta = copy_from.metadata
        if new_path is None:
            folder, file = copy_from.path.rsplit("/", 1)
            new_path = folder + "/Copy-{}".format(file)
            logger.warning(
                "To avoid overwriting original file the new Time Series file will be {},"
                " if you want to overwrite it please specify the new_path explicitly".format(new_path)
            )
        meta["tsPath"] = new_path
        return self.create_time_series(path=new_path, display_name=copy_from.name, attributes=meta)

    @staticmethod
    def is_ensemble(ts) -> bool:
        return any(
            x in ts.metadata["columns"] for x in ["member", "forecast", "dispatchinfo", "dispatch_info"]
        )

    @classmethod
    def are_ensemble(cls, ts_list) -> bool:
        return all(cls.is_ensemble(ts) for ts in ts_list)

    def _get_time_series_list(
        self, ts_filter: str = None, id_list: List[int] = None, params: Mapping[str, Any] = None
    ) -> Iterable[TimeSeries]:
        if ts_filter.startswith("/"):
            raise ValueError("Unexpected leading slash in path, use {}".format(ts_filter[1:]))
        ts_list = []
        for f in self._file_list(self.__root_dir):
            tss = self.__file_format.reader.read(f)

            tss = list(tss)
            if len(tss) > 1:
                stations_to_ids = self._group_indices_by_station(tss)
                for _station, ids in stations_to_ids.items():
                    ts_children = [tss[i] for i in ids]
                    if self.are_ensemble(ts_children):
                        ts_list.append(FileEnsembleTimeSeries.from_timeseries_list(ts_children))
                    else:
                        ts_list.extend(ts_children)
            else:
                ts_list.extend(tss)
        ts_list = self._filter(ts_list, ts_filter)
        ts_list = self._filter_id_list(ts_list, id_list)
        return ts_list

    @staticmethod
    def _group_indices_by_station(ts_list: List[TimeSeries]) -> Mapping[str, Iterable[int]]:
        station_to_indices = {}
        for i in range(len(ts_list)):
            station = ts_list[i].metadata.get("REXCHANGE")
            if station not in station_to_indices:
                station_to_indices[station] = []
            station_to_indices[station].append(i)
        return station_to_indices

    @classmethod
    def _filter(cls, ts_list: Iterable[TimeSeries], ts_filter: str) -> Iterable[TimeSeries]:
        if ts_filter is None:
            return ts_list
        result = []
        exp = re.compile(
            "^"
            + ts_filter.replace(".", "\\.").replace("/", "\\/").replace("?", "\\?").replace("*", ".*")
            + "$"
        )
        for ts in ts_list:
            path = ts.path
            if exp.match(path):
                result.append(ts)
        return result

    @classmethod
    def _filter_id_list(cls, ts_list: Iterable[TimeSeries], id_list: Iterable[int]) -> Iterable[TimeSeries]:
        if id_list is None:
            return ts_list
        result = []
        for ts in ts_list:
            ts_id = ts.id
            if (ts_id is not None) and (ts_id in id_list):
                result.append(ts)
        return result

    def _get_time_series(
        self, ts_id: int = None, path: str = None, params: Mapping[str, Any] = None
    ) -> Union[TimeSeries, None]:
        if path.startswith("/"):
            raise ValueError("Unexpected leading slash in path, use {}".format(path[1:]))
        if params is None:
            params = {"includeDataCoverage": True}
        ts_list = list(
            self._get_time_series_list(ts_filter=path, id_list=[ts_id] if ts_id else None, params=params)
        )
        if len(ts_list) == 0:
            raise KeyError("Requested TimeSeries does not exist.")
        else:
            return ts_list[0]

    def _file_list(self, path: str) -> List[str]:
        file_list = []
        try:
            extensions = self.__file_format.extensions
            for f in sorted(os.listdir(path)):
                if os.path.isfile(path + "/" + f):
                    for e in extensions:
                        if f.lower().endswith("." + e.lower()):
                            file_list.append(path + "/" + f)
                elif os.path.isdir(path + "/" + f):
                    for ff in self._file_list(path + "/" + f):
                        file_list.append(ff)
        except FileNotFoundError:
            return file_list
        return file_list

    def get_by_path(
        self,
        *path: str,
        metadata_keys: Optional[List[str]] = None,
        **kwargs: Mapping,
    ) -> Union[FileTimeSeries, Iterable[FileTimeSeries]]:
        time_series_iter = (self._get_time_series(path=p, params=kwargs.get("params")) for p in path)
        if len(path) == 1:
            return next(time_series_iter)
        else:
            return time_series_iter

    def get_by_filter(
        self,
        *ts_filter: str,
        metadata_keys: Optional[List[str]] = None,
        **kwargs: Mapping,
    ) -> Iterable[FileTimeSeries]:
        time_series_iter = (self._get_time_series_list(ts_filter=tsf) for tsf in ts_filter)
        return (ts for ts_list in time_series_iter for ts in ts_list)

    def read_data_frames(
        self,
        ts_list: Iterable[FileTimeSeries],
        start: Union[str, datetime, Iterable[datetime]] = None,
        end: Union[str, datetime, Iterable[datetime]] = None,
        t0: Union[datetime, Iterable[datetime]] = None,
        dispatch_info: Union[str, Iterable[str]] = None,
        member: Union[str, Iterable[str]] = None,
        **kwargs,
    ) -> Mapping[FileTimeSeries, pd.DataFrame]:
        """
        Read multiple TimeSeries as data frames.

        Args:
            ts_list: An iterable of TimeSeries.
            start: An optional iterable of datetimes representing the date from which data will be written,
                if a single datetime is passed it is used for all the TimeSeries.
            end: An optional iterable of datetimes representing the date until (included) which data will be
                written, if a single datetime is passed it is used for all the TimeSeries.
            t0: An optional iterable of datetimes used to select the t0 in an ensemble TimeSeries, if a
                single datetime is passed it is used for all the TimeSeries.
            dispatch_info: An optional iterable of str used to select the dispatch info in an ensemble
                TimeSeries, if a single str is passed it is used for all the TimeSeries.
            member: An optional iterable of str used to select the member in an ensemble TimeSeries,
                if a single str is passed it is used for all the TimeSeries.
            **kwargs: The additional keyword arguments which are passed to the backend.

        """

        data_frames = {}
        for ts, start_i, end_i, t0_i, dispatch_info_i, member_i in zip(
            ts_list,
            make_iterable(start),
            make_iterable(end),
            make_iterable(t0),
            make_iterable(dispatch_info),
            make_iterable(member),
        ):
            data_frames[ts] = ts.read_data_frame(
                start=start_i,
                end=end_i,
                t0=t0_i,
                dispatch_info=dispatch_info_i,
                member=member_i,
                **kwargs,
            )
        return data_frames

    def transaction(self, *, event_loop: asyncio.AbstractEventLoop = None) -> TimeSeriesTransaction:
        raise NotImplementedError("FileStore only supports 0.7.x API")
