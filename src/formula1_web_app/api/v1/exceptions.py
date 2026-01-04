class DriverNotFoundError(Exception):
    """Exception raised when the requested driver cannot be found in the race results."""

    def __init__(self, driver_id: str) -> None:
        self.driver_id = driver_id


class InvalidDriverIdError(Exception):
    """Exception raised when the provided driver identifier is invalid or malformed."""

    def __init__(self, driver_id: str) -> None:
        self.driver_id = driver_id
