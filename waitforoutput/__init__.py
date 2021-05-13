
import sys
from rkd.api.inputoutput import IO
from .app import WaitForOutputApp, ResultSignal


def main():
    io = IO()

    try:
        args = WaitForOutputApp.parse_args()
        io.set_log_level(args['log_level'])

        WaitForOutputApp(container=args['container'], command=args['command'],
                         pattern=args['pattern'], timeout=int(args['timeout']),
                         io=io) \
            .main()
    except ResultSignal as signal:
        io.info(signal.message) if signal.exit_code == 0 else io.error(signal.message)
        sys.exit(signal.exit_code)

