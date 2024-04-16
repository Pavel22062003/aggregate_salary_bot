import json
from app.services.schemas import ComeInData
from app.settings import db
from app.services.grouping_manager import GroupingManager
from loguru import logger
import re

text = "Невалидный запрос. Пример запроса:\n"
data = {"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}


class AggregateManager:
    def __init__(self, data):
        self.data = data
        self.start_date = None
        self.end_date = None
        self.group_by = None
        self.collection = None

    async def process(self):
        validated_data = await self.validate()
        if validated_data is False:
            return text + json.dumps(data)
        aggregated_data = await self.aggregate_data()
        return json.dumps(await self.format_results(aggregated_data))

    async def validate(self):
        try:
            json_data = json.loads(re.sub(r'\s*(".*?")\s*', r'\1', self.data))
            validated_data = ComeInData(**json_data)
            self.start_date = validated_data.dt_from
            self.end_date = validated_data.dt_upto
            self.group_by = validated_data.group_type
            self.collection = db['sample_collection']

        except Exception as e:
            logger.error(f'validation_error - {e}')
            return False

    async def aggregate_data(self):
        query = {"dt": {"$gte": self.start_date, "$lte": self.end_date}}
        query_data = self.collection.find(query, {'_id': 0, 'value': 1, 'dt': 1})
        core_list = await GroupingManager.build_initial_data(self.start_date, self.end_date, self.group_by.value)
        aggregated_data = await GroupingManager.fill_data_by_dates(data=core_list, query_data=query_data,
                                                                   group_by=self.group_by.value)
        return aggregated_data

    @staticmethod
    async def format_results(aggregated_data):
        return {
            'labels': [v['total'] for v in aggregated_data.values()],
            'dataset': [v.strftime("%Y-%m-%dT%H:%M:%S") for v in aggregated_data.keys()]

        }
