import sys
from .app import WaitForOutputApp, ResultSignal


if __name__ == '__main__':
    args = WaitForOutputApp.parse_args()

    try:
        WaitForOutputApp(container=args['container'], command=args['command'],
                         pattern=args['pattern'], timeout=int(args['timeout']))\
            .main()
    except ResultSignal as signal:
        print(signal.message)
        sys.exit(signal.exit_code)

