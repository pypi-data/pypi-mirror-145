from dnastack import CollectionServiceClient
from dnastack.client.base_exceptions import MissingResourceError
from dnastack.configuration import ServiceEndpoint
from dnastack.helpers.logger import get_logger
from ..exam_helper import ExtendedBaseTestCase


class TestSmoke(ExtendedBaseTestCase):
    _logger = get_logger('lib/smoke_test')

    def test_demo(self):
        """
        This is based on the public documentation.

        .. note:: This test is specifically designed for a certain deployment.
        """
        endpoint = ServiceEndpoint(url='https://viral.ai/api/')
        client = CollectionServiceClient.make(endpoint)

        self._logger.debug('Listing collections...')
        collections = client.list_collections()
        self.assertGreater(len(collections), 0, f'{endpoint.url} should have at least ONE collection.')

        target_collection = collections[0]

        data_connect = client.get_data_connect_client(target_collection)

        self._logger.debug('Listing tables...')
        tables = data_connect.list_tables()
        self.assertGreater(len(tables), 0, f'{target_collection.name} should have at least ONE table.')

        with self.assertRaises(MissingResourceError):
            # This is to confirm that the Table API is not implemented for Viral AI.
            __ = data_connect.table(tables[0]).info

        queried_tables = [r for r in data_connect.query(target_collection.itemsQuery)]

        target_table_name = queried_tables[0]['qualified_table_name']
        if len(target_table_name.split(r'.')) < 3:
            target_table_name = f'ncbi_sra.{target_table_name}'

        self._logger.debug(f'Querying from {target_table_name}...')
        query = f'SELECT * FROM {target_table_name} LIMIT 20000'
        row_count = 0

        for row in data_connect.query(query):
            row_count += 1
            if row_count % 10000 == 0:
                self._logger.debug(f'Receiving {row_count} rows...')
            self.assertGreater(len(row.keys()), 0)
        self._logger.debug(f'Received {row_count} row(s)')

        self.assertGreater(row_count, 0, f'{target_collection} should have at least ONE row.')
