import unittest
import warnings
from rkd.api.inputoutput import IO
from waitforoutput.testing import execute_app
from waitforoutput.app import WaitForOutputApp

warnings.simplefilter("ignore")


class TestWaitForCommand(unittest.TestCase):
    def test_waits_for_output_that_shows_immediately(self):
        io = IO()
        signal = execute_app(
            WaitForOutputApp(container='', command='/bin/bash -c "echo hello"', pattern='hello', timeout=10, io=io)
        )

        self.assertEqual(0, signal.exit_code)
        self.assertEqual('Match found', signal.message)

    def test_waits_for_output_that_shows_after_some_time(self):
        io = IO()
        signal = execute_app(
            WaitForOutputApp(container='', command='/bin/bash -c "sleep 1; echo Yay"',
                             pattern='Yay', timeout=10, io=io)
        )

        self.assertIn('Match found', signal.message)
        self.assertEqual(0, signal.exit_code)

    def test_raises_timeout(self):
        io = IO()
        signal = execute_app(
            WaitForOutputApp(container='', command='/bin/bash -c "sleep 3"',
                             pattern='Yay', timeout=1, io=io)
        )

        self.assertIn('Match not found in expected time of 1s', signal.message)
        self.assertEqual(1, signal.exit_code)
