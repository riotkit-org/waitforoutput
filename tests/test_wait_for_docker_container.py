import unittest
import warnings
from rkd.api.inputoutput import IO
from testcontainers.core.container import DockerContainer
from waitforoutput import WaitForOutputApp
from waitforoutput.testing import execute_app

warnings.simplefilter("ignore")


class TestWaitForDockerContainer(unittest.TestCase):
    def test_waits_for_nginx_to_be_ready(self):
        container = DockerContainer(image='nginx:1.19-alpine').with_name('nginx')
        container.start()

        try:
            io = IO()
            signal = execute_app(
                WaitForOutputApp(container='ngin(.*)', command='',
                                 pattern='Configuration complete; ready for start up', timeout=15, io=io)
            )

            self.assertIn('Match found', signal.message)
            self.assertEqual(0, signal.exit_code)

        finally:
            container.stop()

    def test_regexp_patterns(self):
        container = DockerContainer(image='nginx:1.19-alpine').with_name('nginx_0')
        container.start()

        try:
            io = IO()

            for pattern in ['ngin*', 'nginx.*', 'ng.*x']:
                signal = execute_app(
                    WaitForOutputApp(container=pattern, command='',
                                     pattern='Configuration complete; ready for start up', timeout=15, io=io)
                )

                self.assertIn('Match found', signal.message)
                self.assertEqual(0, signal.exit_code)

        finally:
            container.stop()
