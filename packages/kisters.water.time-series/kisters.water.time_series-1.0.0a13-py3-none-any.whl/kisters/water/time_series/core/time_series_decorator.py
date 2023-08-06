from __future__ import annotations

from datetime import datetime
from typing import Optional, Union

import pandas as pd
import pytz

from kisters.water.time_series.core.time_series import TimeSeries, TimeSeriesMetadata


class TimeSeriesDecorator(TimeSeries):
    def __init__(self, forward: TimeSeries):
        super().__init__(forward.store, forward.columns)
        self._forward = forward
        if hasattr(forward, "_tz"):
            self._tz = forward._tz
        else:
            self._tz = pytz.utc

    @property
    def path(self) -> str:
        return self._forward.path

    @property
    def name(self) -> str:
        return self._forward.name

    @property
    def metadata(self) -> TimeSeriesMetadata:
        return self._forward.metadata

    def coverage_from(
        self,
        t0: Optional[datetime] = None,
        dispatch_info: Optional[str] = None,
        member: Optional[str] = None,
        **kwargs,
    ) -> datetime:
        return self._forward.coverage_from(t0=t0, dispatch_info=dispatch_info, member=member, **kwargs)

    def coverage_until(
        self,
        t0: Optional[datetime] = None,
        dispatch_info: Optional[str] = None,
        member: Optional[str] = None,
        **kwargs,
    ) -> datetime:
        return self._forward.coverage_until(t0=t0, dispatch_info=dispatch_info, member=member, **kwargs)

    def read_data_frame(
        self,
        start: Optional[Union[str, datetime]] = None,
        end: Optional[Union[str, datetime]] = None,
        t0: Optional[datetime] = None,
        dispatch_info: Optional[str] = None,
        member: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        return self._forward.read_data_frame(
            start=start, end=end, t0=t0, dispatch_info=dispatch_info, member=member, **kwargs
        )

    def write_data_frame(
        self,
        data_frame: pd.DataFrame,
        t0: Optional[datetime] = None,
        dispatch_info: Optional[str] = None,
        member: Optional[str] = None,
        **kwargs,
    ):
        return self._forward.write_data_frame(
            data_frame=data_frame, t0=t0, dispatch_info=dispatch_info, member=member, **kwargs
        )
