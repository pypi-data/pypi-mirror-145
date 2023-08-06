import json
import logging
import os.path
import shutil
import subprocess
from json import JSONDecodeError
from typing import Dict

from click.testing import CliRunner, Result

from dnastack.__main__ import dnastack as cli_app
from dnastack.feature_flags import in_global_debug_mode
from dnastack.helpers.environments import env, flag
from dnastack.helpers.logger import get_logger
from ..exam_helper import ExtendedBaseTestCase, ReversibleTestCase


class CliTestCase(ReversibleTestCase, ExtendedBaseTestCase):
    _runner = CliRunner(mix_stderr=False)
    _debug = flag('DNASTACK_DEBUG')
    _config_file_path = env('DNASTACK_CONFIG_FILE')
    _session_dir_path = env('DNASTACK_SESSION_DIR')
    _config_overriding_allowed = flag('E2E_CONFIG_OVERRIDING_ALLOWED')

    def __init__(self, *args, **kwargs):
        super(CliTestCase, self).__init__(*args, **kwargs)
        self._logger = get_logger(f'{type(self).__name__}', self.log_level())

    def log_level(self):
        return logging.DEBUG if in_global_debug_mode else logging.INFO

    def setUp(self) -> None:
        super().setUp()
        self._reset_session()
        self._temporarily_remove_existing_config()

    def tearDown(self) -> None:
        super().tearDown()
        self._reset_session()
        self._restore_existing_config()

    @staticmethod
    def execute(command: str):
        """ Execute a shell script via subprocess directly.

            This is for debugging only. Please use :method:`invoke` for testing.
        """
        subprocess.call(command, shell=True)

    def _invoke(self, *cli_blocks: str) -> Result:
        test_envs = {
            k: 'false' if k == 'DNASTACK_DEBUG' else os.environ[k]
            for k in os.environ
        }
        # noinspection PyTypeChecker
        return self._runner.invoke(cli_app, cli_blocks, env=test_envs)

    def invoke(self, *cli_blocks: str, bypass_error: bool = False) -> Result:
        # noinspection PyTypeChecker
        result = self._invoke(*cli_blocks)
        if hasattr(self, 'show_output') and getattr(self, 'show_output'):
            print(f'EXEC: {" ".join(cli_blocks)}')
            print(f'ERROR:\n{result.stderr}\n')
            print(f'STDOUT:\n{result.stdout}\n')
        if result.exception and not bypass_error:
            raise result.exception
        return result

    def simple_invoke(self, *cli_blocks: str):
        result = self.invoke(*cli_blocks, bypass_error=False)
        self.assertEqual(0, result.exit_code,
                         'The command "' + (' '.join(cli_blocks)) + f'" returns the exit code {result.exit_code}')
        return self.parse_json(result.output)

    @staticmethod
    def parse_json(json_string: str):
        try:
            return json.loads(json_string)
        except JSONDecodeError:
            raise ValueError(f'Unable to parse this JSON string:\n\n{json_string}')

    def _configure(self, config: Dict[str, str], debug=False):
        for k, v in config.items():
            self.invoke('config', 'set', k, v)

        if debug:
            self.execute(f'cat {self._config_file_path}')

    def _temporarily_remove_existing_config(self):
        backup_path = self._config_file_path + '.backup'
        if os.path.exists(self._config_file_path):
            self._logger.debug(f"Detected the existing configuration file {self._config_file_path}.")
            if self._config_overriding_allowed:
                self._logger.debug(f"Temporarily moving {self._config_file_path} to {backup_path}...")
                shutil.copy(self._config_file_path, backup_path)
                os.unlink(self._config_file_path)
                self._logger.debug(f"Successfully moved {self._config_file_path} to {backup_path}.")
            else:
                raise RuntimeError(f'{self._config_file_path} already exists. Please define DNASTACK_CONFIG_FILE ('
                                   f'environment variable) to a different location or E2E_CONFIG_OVERRIDING_ALLOWED ('
                                   f'environment variable) to allow the test to automatically backup the existing '
                                   f'test configuration.')

    def _restore_existing_config(self):
        backup_path = self._config_file_path + '.backup'
        if os.path.exists(backup_path):
            self._logger.debug(f"Restoring {self._config_file_path}...")
            shutil.copy(backup_path, self._config_file_path)
            os.unlink(backup_path)
            self._logger.debug(f"Successfully restored {self._config_file_path}.")

    def _reset_session(self):
        if os.path.exists(self._session_dir_path):
            self._logger.debug("Removing the test session directory...")
            self.execute(f'rm -r{"v" if self._debug else ""} {self._session_dir_path}')
            self._logger.debug("Removed the test session directory.")
