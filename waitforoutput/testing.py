from .app import ResultSignal, WaitForOutputApp


def execute_app(app: WaitForOutputApp) -> ResultSignal:
    signal = ResultSignal(1, '')
    try:
        app.main()
    except ResultSignal as exc:
        signal = exc

    return signal
