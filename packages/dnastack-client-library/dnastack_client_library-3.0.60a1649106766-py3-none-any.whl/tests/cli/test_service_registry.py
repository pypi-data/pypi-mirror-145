from .base import CliTestCase


class TestCliServiceRegistry(CliTestCase):
    def setUpCLI(self):
        self.skipTest("Temporarily disabled - need rewriting")
        self.define_service_registry()
