from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, Iterable, List, Mapping, Optional, TypeVar, Union

from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.core.time_series_metadata import TimeSeriesMetadata
from kisters.water.time_series.core.time_series_decorator import TimeSeriesDecorator
from kisters.water.time_series.core.time_series_store import TimeSeriesStore

T = TypeVar("T")


class CopyableMapping(ABC, Generic[T], Mapping):
    @abstractmethod
    def copy(self: Mapping) -> Mapping:
        # return a copy of self
        raise NotImplementedError


class AddMetadataTimeSeries(TimeSeriesDecorator):
    def __init__(self, backend: AddMetadataStore, ts: TimeSeries):
        super().__init__(ts)
        self._lookup_meta = backend.lookup_metadata(ts.path)

    @property
    def metadata(self) -> TimeSeriesMetadata:
        if self._lookup_meta is None:
            meta = {}
        else:
            meta = self._lookup_meta.copy()
        meta.update(super().metadata)
        return meta


class AddMetadataStore(TimeSeriesStore):
    """
    AddMetadataStore is a TimeSeriesStore decorator which allows to add metadata
    to TimeSeries inside the original TimeSeriesStore. To add metadata you must
    provide a Mapping of paths to metadata dictionaries.

    Args:
        forward: The TimeSeriesStore to be decorated.
        metadata: The mapping providing metadata. Keys are the time series paths,
                  and values are the metadata maps for each time series.

    Example:
        .. code-block:: python

            import json
            from kisters.water.file_io import FileStore, ZRXPFormat
            from kisters.water.store_decorators import AddMetadataStore
            with open('tests/data/addmetadata.json', 'r') as f:
                j = json.load(f)
            store = AddMetadataStore(FileStore('tests/data', ZRXPFormat()), j)
            ts = store.get_by_path('validation/threshold/05BJ004.HG.datum.O')
            ts.metadata['THRESHOLDATTR']
    """

    def __init__(self, forward: TimeSeriesStore, metadata: Mapping[str, Any]):
        self._forward = forward
        self.__metadata = metadata

    def create_time_series(
        self, path: str, display_name: str, attributes: Mapping[str, Any] = None, params: Mapping = None
    ) -> TimeSeries:
        meta = self.lookup_metadata(path)
        meta = {} if meta is None else meta
        attributes = {} if attributes is None else attributes
        attributes.update(meta)
        return self._forward.create_time_series(path, display_name, attributes, params)

    def get_by_filter(
        self,
        *ts_filter: str,
        metadata_keys: Optional[List[str]] = None,
        **kwargs: Mapping,
    ) -> Iterable[AddMetadataTimeSeries]:
        ts_list = self._forward.get_by_filter(*ts_filter, metadata_keys=metadata_keys, **kwargs)
        ts_list = [AddMetadataTimeSeries(self, ts) for ts in ts_list]
        return ts_list

    def get_by_path(
        self,
        *path: str,
        metadata_keys: Optional[List[str]] = None,
        **kwargs: Mapping,
    ) -> Union[AddMetadataTimeSeries, Iterable[AddMetadataTimeSeries]]:
        time_series_list = self._forward.get_by_path(*path, metadata_keys=metadata_keys, **kwargs)
        if isinstance(time_series_list, TimeSeries):
            return AddMetadataTimeSeries(self, time_series_list)
        else:
            return [AddMetadataTimeSeries(self, ts) for ts in time_series_list]

    def transaction(self):
        return self._forward.transaction()

    def lookup_metadata(self, path: str) -> Optional[CopyableMapping]:
        if path in self.__metadata:
            return self.__metadata[path]
        return None
