import re
from pydantic import BaseModel
from requests import Response
from time import time
from typing import List, Optional, Union
from urllib.parse import urljoin

from .base_client import BaseServiceClient
from .dataconnect_client import DataConnectClient
from ..configuration import ServiceEndpoint
from ..exceptions import ServiceException


def _raise_error(url: str, res: Response, primary_reason: str):
    summary = f'Unexpected Error: HTTP {res.status_code}'
    detail = primary_reason

    if res.status_code == 401:
        summary = "Authentication Required"
    elif res.status_code == 403:
        summary = "Access Denied"
    elif res.status_code == 404:
        summary = "Not Found"
    else:
        response_json = res.json()
        if 'message' in response_json:
            # Handle a generic error response from the service.
            detail += f' ({response_json["message"]})'
        elif "errors" in response_json and response_json['errors'] and 'title' in response_json['errors'][0]:
            detail += f' ({", ".join([e["title"] for e in response_json["errors"]])})'
        else:
            detail += f' ({response_json})'

    raise ServiceException(msg=f'{summary}: {detail}', url=url)


class UnsupportedClientModeError(RuntimeError):
    """ Raised when the specified mode is incompatible or supported """


class Collection(BaseModel):
    """
    A model representing a collection

    .. note:: This is not a full representation of the object.
    """

    id: Optional[str]
    name: str
    slugName: str
    description: Optional[str]
    itemsQuery: str

    @classmethod
    def make(cls,
             name: str,
             items_query: str,
             slug_name: Optional[str] = None,
             description: Optional[str] = None):
        if not slug_name:
            slug_name = re.sub(r'[^a-z0-9-]', '-', name.lower()) + str(int(time()))
            slug_name = re.sub(r'-+', '-', slug_name)
        return cls(name=name, itemsQuery=items_query, slugName=slug_name, description=description)


class CollectionServiceClient(BaseServiceClient):
    """Client for Collection API"""

    def __init__(self, endpoint: ServiceEndpoint):
        if not endpoint.url.endswith(r'/'):
            endpoint.url = endpoint.url + r'/'

        super(CollectionServiceClient, self).__init__(endpoint)

    @staticmethod
    def get_adapter_type() -> str:
        return 'collections'

    def _get_single_collection_url(self, id_or_slug_name: str, extended_path: str = ''):
        if self._endpoint.mode == 'standard':
            return urljoin(self.url, f'collection/{id_or_slug_name}{extended_path}')
        if self._endpoint.mode == 'explorer':
            return urljoin(self.url, f'collections/{id_or_slug_name}{extended_path}')
        else:
            raise UnsupportedClientModeError(self._endpoint.mode)

    def get(self, id_or_slug_name: str) -> Collection:
        """ Get a collection by ID or slug name """
        get_response = self.client.get(self._get_single_collection_url(id_or_slug_name))
        if not get_response.ok:
            _raise_error(self.url, get_response, 'Collection not found')

        return Collection(**get_response.json())

    def list_collections(self) -> List[Collection]:
        """ List all available collections """
        res = self.client.get(urljoin(self.url, 'collections'))

        if not res.ok:
            _raise_error(self.url, res, "Unable to list collections")

        return [Collection(**raw_collection) for raw_collection in res.json()]

    def get_data_connect_client(self, collection: Union[str, Collection]) -> DataConnectClient:
        """ Get the Data Connect client for the given collection (ID, slug name, or collection object) """
        # noinspection PyUnusedLocal
        collection_id = None

        if isinstance(collection, Collection):
            collection_id = collection.slugName
        elif isinstance(collection, str):
            collection_id = collection
        else:
            raise TypeError(f'Unexpected type: {type(collection).__name__}')

        sub_endpoint = ServiceEndpoint(**self._endpoint.dict())
        sub_endpoint.url = self._get_single_collection_url(collection_id, '/data-connect/')

        return DataConnectClient.make(sub_endpoint)


# Temporarily for backward compatibility
CollectionsClient = CollectionServiceClient
