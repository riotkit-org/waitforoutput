
import re
import sys
import argparse
import multiprocessing
from subprocess import check_output
from rkd.process import check_call


class OccurrenceFoundSignal(Exception):
    pass


class ContainerNotFound(Exception):
    pass


class ResultSignal(Exception):
    exit_code: int
    message: str

    def __init__(self, exit_code: int, message: str):
        self.exit_code = exit_code
        self.message = message


class WaitForOutputApp(object):
    container: str
    command: str
    pattern: str
    timeout: int

    def __init__(self, container: str, command: str, pattern: str, timeout: int):
        self.container = container
        self.command = command
        self.pattern = pattern
        self.timeout = timeout

    def main(self):
        if self.container:
            try:
                self.container = self.find_container_name(self.container)
            except ContainerNotFound:
                print('No any container matches pattern "{}"'.format(self.container))
                sys.exit(1)

            self.command = 'docker logs -f {}'.format(self.container)

        manager = multiprocessing.Manager()
        results_dict = manager.dict()

        # use multiprocessing to spawn a process that will HAVE A TIMEOUT
        proc = multiprocessing.Process(target=self.wait_for_command_output, args=(
            self.pattern, self.command, results_dict
        ))
        proc.start()
        proc.join(timeout=self.timeout)

        if proc.is_alive():
            raise ResultSignal(1, 'Match not found in expected time of {}s'.format(self.timeout))

        if results_dict.get('found', None) is True:
            raise ResultSignal(0, 'Match found')
        else:
            raise ResultSignal(1, 'Match not found, process exited earlier')

    @staticmethod
    def wait_for_command_output(pattern: str, command: str, results: dict):
        def is_command_output_matching(text: str):
            if re.findall(pattern, text):
                raise OccurrenceFoundSignal()

        try:
            check_call(command, output_capture_callback=is_command_output_matching)

        except OccurrenceFoundSignal:
            results['found'] = True
            return

        results['found'] = False

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--container', '-c', default='', help='Container name/regexp')
        parser.add_argument('--command', '-cmd', default='', help='Command to watch')
        parser.add_argument('--timeout', '-t', default='30', help='Timeout')
        parser.add_argument('pattern', help='Pattern to search for in command output')

        parsed = parser.parse_args()

        if parsed.container and parsed.command:
            raise ResultSignal(1, 'Please specify one of --container or --command')

        return vars(parsed)

    @staticmethod
    def find_container_name(pattern: str) -> str:
        running_containers = check_output(["docker", "ps", "--format", "{{.Names}}"]).decode('utf-8').split("\n")

        for container in running_containers:
            if re.match(pattern, container):
                return container

        raise ContainerNotFound()
