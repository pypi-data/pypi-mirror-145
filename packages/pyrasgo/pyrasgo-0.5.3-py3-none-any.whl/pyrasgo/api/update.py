import time
from typing import List, Optional, Union

from snowflake.connector import ProgrammingError

from pyrasgo.utils.versioning import deprecated_without_replacement
from .error import APIError
from pyrasgo import schemas
from pyrasgo import primitives


class Update:

    def __init__(self):
        from . import Get
        from .connection import Connection
        from pyrasgo.config import get_session_api_key
        from pyrasgo.storage import DataWarehouse, SnowflakeDataWarehouse

        api_key = get_session_api_key()
        self.api = Connection(api_key=api_key)
        self.get = Get()
        self.data_warehouse: SnowflakeDataWarehouse = DataWarehouse.connect()

    @deprecated_without_replacement('v1.0')
    def collection_attributes(self,
                              id: int,
                              attributes: List[dict]):
        """
        Create or update attributes on a Rasgo Collection

        param attributes: dict [{"key": "value"}, {"key": "value"}]
        """
        msg = 'attributes parameter must be passed in as a list of k:v pairs. Example: [{"key": "value"}, {"key": "value"}]'
        if not isinstance(attributes, list):
            raise APIError(msg)
        attr = []
        for kv in attributes:
            if not isinstance(kv, dict):
                raise APIError(msg)
            for k, v in kv.items():
                attr.append(schemas.Attribute(key=k, value=v))
        attr_in = schemas.CollectionAttributeBulkCreate(collectionId = id, attributes=attr)
        return self.api._put(f"/models/{id}/attributes", attr_in.dict(exclude_unset=True), api_version=1).json()

    @deprecated_without_replacement('v1.0')
    def data_source(self,
                    id: int,
                    name: Optional[str] = None,
                    domain: Optional[str] = None,
                    source_type: Optional[str] = None,
                    table: Optional[str] = None,
                    database: Optional[str] = None,
                    schema: Optional[str] = None,
                    source_code: Optional[str] = None,
                    table_status: Optional[str] = None,
                    parent_source_id: Optional[int] = None) -> primitives.DataSource:
        data_source = schemas.DataSourceUpdate(id=id,
                                           name=name,
                                           domain=domain,
                                           table=table,
                                           tableDatabase=database,
                                           tableSchema=schema,
                                           sourceCode=source_code,
                                           tableStatus=table_status,
                                           sourceType=source_type,
                                           parentId=parent_source_id)
        response = self.api._patch(f"/data-source/{id}", data_source.dict(exclude_unset=True, exclude_none=True), api_version=1).json()
        return primitives.DataSource(api_object=response)

    @deprecated_without_replacement('v1.0')
    def dataframe(self,
                  unique_id: str,
                  name: Optional[str] = None,
                  shared_status: str = None,
                  column_hash: str = None,
                  update_date: str = None) -> schemas.Dataframe:
        if shared_status not in [None, 'private', 'organization', 'public']:
            raise APIError("Valid values for shared_status are ['private', 'organization', 'public']")
        dataframe = schemas.DataframeUpdate(name=name,
                                        uniqueId=unique_id,
                                        sharedStatus=shared_status,
                                        columnHash=column_hash,
                                        updatedDate = update_date)
        response = self.api._patch(f"/dataframes/{unique_id}", dataframe.dict(exclude_unset=True, exclude_none=True), api_version=1).json()
        return schemas.Dataframe(**response)

    @deprecated_without_replacement('v1.0')
    def feature(self,
                id: int,
                display_name: Optional[str] = None,
                column_name: Optional[str] = None,
                description: Optional[str] = None,
                status: Optional[str] = None,
                tags: Optional[List[str]] = None,
                git_repo: Optional[str] = None) -> primitives.Feature:
        feature = schemas.FeatureUpdate(id=id,
                                    name=display_name,
                                    code=column_name,
                                    description=description,
                                    orchestrationStatus=status,
                                    tags=tags,
                                    gitRepo=git_repo)
        response = self.api._patch(f"/features/{id}", feature.dict(exclude_unset=True, exclude_none=True), api_version=1).json()
        return primitives.Feature(api_object=response)

    @deprecated_without_replacement('v1.0')
    def feature_attributes(self,
                           id: int,
                           attributes: List[dict]):
        """
        Create or update attributes on a feature

        param attributes: dict [{"key": "value"}, {"key": "value"}]
        """
        msg = 'attributes parameter must be passed in as a list of k:v pairs. Example: [{"key": "value"}, {"key": "value"}]'
        if not isinstance(attributes, list):
            raise APIError(msg)
        attr = []
        for kv in attributes:
            if not isinstance(kv, dict):
                raise APIError(msg)
            for k, v in kv.items():
                attr.append(schemas.Attribute(key=k, value=v))
        attr_in = schemas.FeatureAttributeBulkCreate(
            featureId = id,
            attributes=attr
        )
        return self.api._put(f"/features/{id}/attributes", attr_in.dict(exclude_unset=True), api_version=1).json()

    def transform(
            self,
            transform_id: int,
            name: Optional[str] = None,
            source_code: Optional[str] = None,
            type: Optional[str] = None,
            arguments: Optional[List[dict]] = None,
            description: Optional[str] = None,
            tags: Optional[Union[List[str], str]] = None
    ) -> schemas.Transform:
        """
        Updates a transform in Rasgo

        Args:
            transform_id: Id of transform to update
            name: Name of the Transform
            source_code: Source code of transform
            type: Type of transform it is. Used for categorization only
            arguments: A list of arguments to supply to the transform
                       so it can render them in the UI. Each argument
                       must be a dict with the keys: 'name', 'description', and 'type'
                       values all strings for their corresponding value
            description: Description of Transform
            tags: List of tags, or a tag (string), to set on this dataset
        """
        # Init tag array to be list of strings
        if tags is None:
            tags = []
        elif isinstance(tags, str):
            tags = [tags]

        # Make request to update transform and return
        transform_update = schemas.TransformUpdate(
            name=name,
            type=type,
            description=description,
            sourceCode=source_code,
            arguments=arguments,
            tags=tags
        )
        response = self.api._put(
            f"/transform/{transform_id}",
            transform_update.dict(exclude_unset=True, exclude_none=True),
            api_version=1
        ).json()
        return schemas.Transform(**response)

    def dataset(
            self,
            dataset: primitives.Dataset,
            *,
            name: Optional[str] = None,
            description: Optional[str] = None,
            attributes: Optional[dict] = None,
    ) -> primitives.Dataset:
        """
        Update a dataset name, description, and/or attributes in Rasgo
        """
        # Raise error if trying to update a dataset in offline mode
        if not dataset._api_dataset:
            raise APIError("Can not update dataset. Needs to be saved first with `rasgo.save.dataset()`")

        dataset_update = schemas.DatasetUpdate(
            # Possible Changed Fields
            name=name,
            description=description,
            # Persist other fields in update contract so no fields set to None in update
            status=dataset._api_dataset.status,
            owner_id=dataset._api_dataset.owner_id,
            dw_table_id=dataset._api_dataset.dw_table_id,
            attributes=attributes
        )
        response = self.api._put(
            f"/datasets/{dataset._api_dataset.id}",
            dataset_update.dict(exclude_unset=True, exclude_none=True),
            api_version=2
        ).json()
        dataset_schema = schemas.Dataset(**response)
        return primitives.Dataset(
            api_dataset=dataset_schema
        )

    def dataset_table(
            self,
            dataset: primitives.Dataset,
            verbose: bool = False
    ) -> None:
        """
        Kicks off a query for re-materializing a dataset's set Dw Table.

        The dataset needs to be published first in order call this function

        Args:
            dataset: Published dataset to refresh table for
            verbose: If True will print information related to refreshing table
        """
        # We need to ensure that the API dataset is exists and is published
        if (not dataset._api_dataset or dataset.status.lower() != "published"):
            raise APIError('Can not refresh table. Dataset must first be published')

        if verbose:
            print(f"Refreshing table for dataset with id '{dataset.id}' at fqtn: '{dataset.fqtn}'")


        # Call endpoint to kick off Query to re-create table in background
        sf_query_id = self.api._put(
            f"/datasets/{dataset._api_dataset.id}/table-refresh",
            _json={'refreshInBackground': True},
            api_version=2
        ).json()
        conn = self.data_warehouse.user_connection
        while conn.is_still_running(conn.get_query_status_throw_if_error(sf_query_id)):
            if verbose:
                print("Query still executing...")
            time.sleep(1)

        if verbose:
            print(f"Done Refreshing table for dataset with id '{dataset.id}' at fqtn: '{dataset.fqtn}'")


    def column(
            self,
            dataset_column_id: int,
            display_name: Optional[str] = None,
            description: Optional[str] = None,
            attributes: Optional[dict] = None,
            tags: Optional[List[str]] = None
    ) -> schemas.DatasetColumn:
        """
        Update metadata about a dataset column

        Args:
            dataset_column_id: Dataset column id to updated. Use `dataset.columns[x].id` to retrieve
            display_name: Display name to update for this dataset column if set
            description: Description to update for this dataset column if set
            attributes: Attributes to add or update for this dataset column. Set as Key Value pairs dict
            tags: Tags to add to this dataset column

        Returns:
            Updated Dataset Column Obj
        """
        ds_col_update = schemas.DatasetColumnUpdate(
            display_name=display_name,
            description=description,
            attributes=attributes,
            tags=tags
        )
        resp = self.api._put(
            f"/dataset-columns/{dataset_column_id}",
            ds_col_update.dict(exclude_unset=True, exclude_none=True),
            api_version=2
        ).json()
        return schemas.DatasetColumn(**resp)
