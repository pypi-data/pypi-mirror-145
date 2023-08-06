from unittest import TestCase

from dnastack.helpers.environments import env


class TestCliWesCommand(TestCase):
    def setUp(self):
        self.skipTest("Temporarily disabled - incomplete configuration")

        self.wes_url = env('E2E_WES_URL', required=True)
        self.client_id = env('E2E_WES_CLIENT_ID', required=True)
        self.client_secret = env('E2E_WES_CLIENT_SECRET', required=True)

        # TODO fill in more client-credential auth configuration.
        # ...
