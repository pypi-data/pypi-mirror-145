class SporeStackError(Exception):
    pass


class SporeStackUserError(SporeStackError):
    """HTTP 4XX"""

    pass


class SporeStackServerError(SporeStackError):
    """HTTP 5XX"""

    pass
