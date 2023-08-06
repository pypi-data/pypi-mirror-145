from enum import IntEnum, unique

from sqlalchemy import func
from sqlalchemy.orm import Query, Session

import model as m
from cas.data import Session as SessionFunc
from cas.utils import has_value


@unique
class BimDataModelType(IntEnum):
    Architectural = 1 << 0
    Structural = 1 << 1
    Mep = 1 << 2
    Custom = 1 << 3


@unique
class BimDataModelPhase(IntEnum):
    PreConstruction = 0
    Construction = 1
    PostConstruction = 2
    Refurbishment = 3


@unique
class BimDataModelState(IntEnum):
    Initialising = 0,
    Ready = 1,
    Updating = 2,
    Error = 3


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

    def get_model_file_name(self, project_id: str, organisation_id: str,
                            file_type: BimDataModelFileType = BimDataModelFileType.Ifc):
        model_query = self.__default_model_query(project_id, organisation_id)
        file = self.__generate_model_file_query(model_query, filter_file_type=file_type).first()
        if file is None:
            return None

        file_name = f'{file.ModelId}_{file.VersionNumber}'
        if has_value(file.FileNameSuffix):
            file_name = f'{file_name}_{file.FileNameSuffix}'

        return file_name

    def find_default_model(self, project_id: str, organisation_id: str) -> m.BimDataModel:
        return self.__default_model_query(project_id, organisation_id).first()

    def __default_model_query(self, project_id: str, organisation_id: str) -> Query:
        return self.__generate_model_query(fileter_project_id=project_id,
                                           filter_organisation_id=organisation_id,
                                           filter_model_type=BimDataModelType.Architectural,
                                           filter_model_state=BimDataModelState.Ready,
                                           filter_by_default_model=True)

    def __generate_model_query(self,
                               fileter_project_id: str,
                               filter_organisation_id: str,
                               filter_model_id: str = None,
                               filter_model_type: BimDataModelType = None,
                               filter_model_phase: BimDataModelPhase = None,
                               filter_model_state: BimDataModelState = None,
                               filter_by_default_model: bool = False) -> Query:
        """Will apply the query parameters to the Query. If the query is None, a new query will be generated from the
        Session."""
        result = self.__session.query(m.BimDataModel)

        if has_value(fileter_project_id):
            result = result.filter(m.BimDataModel.ProjectId == fileter_project_id)

        if has_value(filter_organisation_id):
            result = result.filter(m.BimDataModel.OrganisationId == filter_organisation_id)

        if filter_model_type is not None:
            result = result.filter(m.BimDataModel.ModelType == int(filter_model_type))

        if filter_model_phase is not None:
            result = result.filter(m.BimDataModel.ModelPhase == int(filter_model_phase))

        if filter_model_state is not None:
            result = result.filter(m.BimDataModel.ModelState == int(filter_model_state))

        if has_value(filter_model_id):
            result = result.filter(m.BimDataModel.ModelId == filter_model_id)
        elif filter_by_default_model:
            result = result.filter(m.BimDataModel.IsDefault)

        return result

    def __generate_model_version_query(self,
                                       model_query: Query,
                                       filter_version_number: int = None) -> Query:
        sub_q = model_query.subquery(name='bim_model')
        result = self.__session.query(m.BimDataModelVersion).join(sub_q,
                                                                  m.BimDataModelVersion.ModelId == sub_q.c.ModelId)

        if filter_version_number is not None:
            result = result.filter(m.BimDataModelVersion.VersionNumber == filter_version_number)

        return result

    def __generate_model_file_query(self,
                                    model_query: Query,
                                    filter_file_type: BimDataModelFileType = None,
                                    filter_latest_file: bool = True) -> Query:
        sub_model_q = model_query.subquery(name='bim_model')
        result = self.__session.query(m.BimDataModelVersionFile) \
            .join(sub_model_q, m.BimDataModelVersionFile.ModelId == sub_model_q.c.ModelId)

        if filter_file_type is not None:
            result = result.filter(m.BimDataModelVersionFile.BimModelFileType == int(filter_file_type))

        if filter_latest_file:
            max_query = self.__session.query(func.max(m.BimDataModelVersionFile.VersionNumber))
            result = result.filter(m.BimDataModelVersionFile.VersionNumber == max_query)
            pass

        return result


if __name__ == '__main__':
    with SessionFunc() as session:
        repo = BimDataModelRepository(sql_session=session)
        model = repo.get_model_file_name('11220000-4800-acde-c6da-08da1619d625', 'CAS')

        print('Found', model)
