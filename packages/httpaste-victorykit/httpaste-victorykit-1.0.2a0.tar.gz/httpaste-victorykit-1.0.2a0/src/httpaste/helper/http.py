
class BadRequestError(RuntimeError):
    def __init__(self, msg=None):
        super().__init__(msg)

    @staticmethod
    def render(error):
        return {
            "detail": str(error),
            "status": 400,
            "title": "Bad Request",
        }, 400


class UnauthorizedError(RuntimeError):
    def __init__(self, msg=None):
        super().__init__(msg)

    @staticmethod
    def render(error):
        return {
            "detail": str(error),
            "status": 401,
            "title": "Unauthorized s",
        }, 401


class ForbiddenError(RuntimeError):
    def __init__(self, msg=None):
        super().__init__(msg)

    @staticmethod
    def render(error):
        return {
            "detail": str(error),
            "status": 403,
            "title": "Forbidden",
        }, 403


class GoneError(RuntimeError):
    def __init__(self, msg=None):
        super().__init__(msg)

    @staticmethod
    def render(error):
        return {
            "detail": str(error),
            "status": 410,
            "title": "Gone",
        }, 410


class NotFoundError(RuntimeError):
    def __init__(self, msg=None):
        super().__init__(msg)

    @staticmethod
    def render(error):
        return {
            "detail": str(error),
            "status": 404,
            "title": "Not Found",
        }, 404
