from dnastack.helpers.environments import env

from .base import CliTestCase
from .utils import *


class TestCliWesCommand(CliTestCase):
    def setUp(self):
        super().setUp()

        self.skipTest("Temporarily disabled - incomplete configuration")

        self.wes_url = env('E2E_WES_URL', required=True)

        self.invoke('config', 'set', 'wes.url', env('E2E_WES_URL', required=True))
        self.invoke('config', 'set', 'wes.authentication.oauth2.client_id', env('E2E_WES_CLIENT_ID', required=True))
        self.invoke('config', 'set', 'wes.authentication.oauth2.client_secret', env('E2E_WES_CLIENT_SECRET', required=True))
        # TODO fill in more client-credential auth configuration.
        # ...

    def test_wes_info_with_auth(self):
        result_objects = self.simple_invoke("wes", "info")

        assert_has_property(self, result_objects, "workflow_type_versions")
        assert_has_property(self, result_objects, "supported_wes_versions")
        assert_has_property(self, result_objects, "supported_filesystem_protocols")
        assert_has_property(self, result_objects, "workflow_engine_versions")
        assert_has_property(self, result_objects, "system_state_counts")
