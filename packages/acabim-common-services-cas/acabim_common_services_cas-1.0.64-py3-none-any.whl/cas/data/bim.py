from dataclasses import dataclass
from enum import IntEnum, unique

from sqlalchemy.orm import Query, Session

import model as m
from cas.data import Session as SessionFunc
from cas.utils import has_value


@dataclass
class BuildingModelQueryParams:
    fileter_project_id: str = None
    filter_model_id: str = None
    filter_by_default_model: bool = False


@unique
class BimDataModelFileType(IntEnum):
    Unknown = 0
    ThreeDModel = 1
    TwoDModel = 2
    Ifc = 3
    Csv = 4
    BlueprintJson = 5


class BimDataModelRepository:

    def __init__(self, sql_session: Session):
        self.__session = sql_session

    def get_ifc_file(self):
        pass

    def find_default_model(self, project_id: str) -> m.BimDataModel:
        params = BuildingModelQueryParams(fileter_project_id=project_id,
                                          filter_by_default_model=True)
        query = self.__generate_query(params=params)
        return query.first()

    def __generate_query(self, params: BuildingModelQueryParams = None) -> Query:
        """Will apply the query parameters to the Query. If the query is None, a new query will be generated from the
        Session."""
        result = self.__session.query(m.BimDataModel)
        if params is None:
            return result

        if has_value(params.filter_model_id):
            result = result.filter(m.BimDataModel.ModelId == params.filter_model_id)
        elif params.filter_by_default_model:
            result = result.filter(m.BimDataModel.IsDefault)

        if has_value(params.fileter_project_id):
            result = result.filter(m.BimDataModel.ProjectId == params.fileter_project_id)

        return result


if __name__ == '__main__':
    with SessionFunc() as session:
        repo = BimDataModelRepository(sql_session=session)
        model = repo.find_default_model('11220000-4800-acde-c6da-08da1619d625')

        print('Found', model)
