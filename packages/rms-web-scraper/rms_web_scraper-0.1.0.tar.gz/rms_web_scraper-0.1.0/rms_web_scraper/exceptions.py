class ScraperException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class FormNotFound(ScraperException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NoInputs(ScraperException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class SessionError(ScraperException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnconfiguredReport(ScraperException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)