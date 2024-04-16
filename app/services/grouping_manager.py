from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Callable

from dateutil.relativedelta import relativedelta


@dataclass
class GroupingData:
    find_start_date: Callable
    append_delta: relativedelta


grouping_values = {
    'week': GroupingData(
        find_start_date=lambda x: x - timedelta(days=x.weekday()),
        append_delta=relativedelta(weeks=1)
    ),
    'day': GroupingData(
        find_start_date=lambda x: x.replace(hour=0, minute=0, microsecond=0, second=0),
        append_delta=relativedelta(days=1)
    ),
    'hour': GroupingData(
        find_start_date=lambda x: x.replace(minute=0, microsecond=0, second=0),
        append_delta=relativedelta(hours=1)
    ),
    'month': GroupingData(
        find_start_date=lambda x: x.replace(day=1, hour=0, minute=0, microsecond=0, second=0),
        append_delta=relativedelta(months=1)
    )
}


class GroupingManager:
    @staticmethod
    async def build_initial_data(start_date: datetime, end_date: datetime, group_by: str, dict_data=None):
        results = {}
        grouping_data: GroupingData = grouping_values.get(group_by)
        _start_date = grouping_data.find_start_date(start_date)
        dict_data = dict_data or {'total': 0}
        while _start_date <= end_date:
            _value = {'date': str(_start_date)}
            _value.update(dict_data)
            results[_start_date] = _value
            _start_date += grouping_data.append_delta
        current_values = list(results.values())
        count = len(current_values)
        if not count:
            return results
        if current_values[0]['date'] < str(start_date):
            current_values[0]['date'] = str(start_date)
        if current_values[count - 1]['date'] > str(end_date):
            current_values[count - 1]['date'] = str(end_date)
        return results

    @staticmethod
    def build_keys(start_date: datetime, end_date: datetime, group_by: str):
        results = []
        grouping_data: GroupingData = grouping_values.get(group_by)
        _start_date = grouping_data.find_start_date(start_date)
        while _start_date <= end_date:
            results.append(_start_date)
            _start_date += grouping_data.append_delta
        return results

    @staticmethod
    async def fill_data_by_dates(data: dict, query_data, group_by):
        async for el in query_data:
            key = GroupingManager.get_key_by_date(el['dt'], group_by)
            if key in data:
                data[key]['total'] += el['value']
        return data

    @staticmethod
    def get_key_by_date(date: datetime, group_by: str):
        grouping_data: GroupingData = grouping_values.get(group_by)
        return grouping_data.find_start_date(date)

