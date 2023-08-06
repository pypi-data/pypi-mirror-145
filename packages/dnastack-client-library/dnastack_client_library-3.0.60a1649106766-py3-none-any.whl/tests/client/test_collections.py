import re
from time import time

from dnastack.client.collections_client import CollectionServiceClient, Collection
from dnastack.client.dataconnect_client import DataConnectClient
from dnastack.exceptions import ServiceException
from dnastack.helpers.environments import env
from ..exam_helper import initialize_test_endpoint, ReversibleTestCase, ExtendedBaseTestCase


class TestCollectionsClient(ReversibleTestCase, ExtendedBaseTestCase):
    """ Test a client for Collection Service """

    # Test-specified
    collection_endpoint = initialize_test_endpoint(CollectionServiceClient.get_adapter_type(),
                                                   env('E2E_COLLECTION_SERVICE_URL',
                                                       default='https://collection-service.viral.ai/'))
    data_connect_endpoint = initialize_test_endpoint(DataConnectClient.get_adapter_type(),
                                                     env('E2E_PROTECTED_DATA_CONNECT_URL',
                                                         default='https://data-connect-trino.viral.ai/'))

    def test_auth_client_interacts_with_collection_api(self):
        collection_client = CollectionServiceClient.make(self.collection_endpoint)

        collections = collection_client.list_collections()

        self.assertGreater(len(collections), 0)
        self.assertIsInstance(collections[0], Collection)
        collection = collections[0]
        self.assert_not_empty(collection.id)
        self.assert_not_empty(collection.slugName)

        with self.assertRaisesRegex(ServiceException, 'Collection not found'):
            collection_client.get('foo-bar')

    def test_auth_client_interacts_with_data_connect_api(self):
        re_table_type = re.compile(r"type\s*=\s*'table'")

        collection_client = CollectionServiceClient.make(self.collection_endpoint)

        collections = collection_client.list_collections()
        self.assert_not_empty(collections)

        target_collection = [c for c in collections if re_table_type.search(c.itemsQuery)][0]

        # New APIs
        collection_data_connect_client = collection_client.get_data_connect_client(target_collection)
        tables = collection_data_connect_client.list_tables()
        self.assert_not_empty(tables)
        first_table = tables[0]
        self.assert_not_empty([row for row in collection_data_connect_client.query(f'SELECT * FROM {first_table.name} LIMIT 10')])
