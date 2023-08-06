from typing import Union, Optional, Dict, Type, TypeVar

from imagination.decorator import service

from dnastack.client.base_client import BaseServiceClient
from dnastack.client.collections_client import CollectionServiceClient
from dnastack.client.dataconnect_client import DataConnectClient
from dnastack.client.files_client import DrsClient
from dnastack.client.wes_client import WesClient
from dnastack.configuration import ConfigurationManager, ServiceEndpoint, MissingEndpointError

_C = TypeVar('_C', bound=BaseServiceClient)


@service.registered()
class ClientManager:
    _client_type_to_cls_map: Dict[str, Type[_C]] = {
        cls.get_adapter_type(): cls
        for cls in [CollectionServiceClient, DataConnectClient, DrsClient, WesClient]
    }

    def __init__(self, config_manager: ConfigurationManager):
        self.__config_manager = config_manager

    def get(self, id: str) -> BaseServiceClient:
        config = self.__config_manager.load()
        endpoint: Optional[ServiceEndpoint] = None

        for iterated_endpoint in config.endpoints:
            if iterated_endpoint.id == id:
                endpoint = iterated_endpoint
                break

        if endpoint.adapter_type in self._client_type_to_cls_map:
            return self._client_type_to_cls_map[endpoint.adapter_type].make
        else:
            raise MissingEndpointError(id)
