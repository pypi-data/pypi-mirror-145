from dataclasses import dataclass

from sqlalchemy.orm import Query
from cas.utils import has_value
import model as m
import cas.data as data


@dataclass
class BuildingModelQueryParams:
    fileter_project_id: str = None
    filter_model_id: str = None


class BimDataModelRepository:

    def find_models(self, params: BuildingModelQueryParams = BuildingModelQueryParams()) -> m.BimDataModel:
        with data.Session() as session:
            query = BimDataModelRepository.__apply_filter(session.query(m.BimDataModel), params)
            return query.all()

    @staticmethod
    def __apply_filter(query: Query, params: BuildingModelQueryParams) -> Query:
        result = query
        if has_value(params.filter_model_id):
            result = result.filter(m.BimDataModel.ModelId == params.filter_model_id)

        if has_value(params.fileter_project_id):
            result = result.filter(m.BimDataModel.ProjectId == params.fileter_project_id)

        return result


if __name__ == '__main__':
    q_params = BuildingModelQueryParams(fileter_project_id='11220000-4800-acde-c6da-08da1619d625')
    items = BimDataModelRepository().find_models(q_params)

    print('Found', items)