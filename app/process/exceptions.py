class TooMuchImagesError(Exception):
    """
        Raise an error when user uploads more than 5 images
    """
    def _init_(self, user: str, message: str):
        Exception._init_(self, message)
        self.user: str = user


class UserProcessError(Exception):
    """
        Raise a user error
    """

    def _init_(self, message: str, status_code: int):
        Exception._init_(self, message)
        self.status_code = status_code


class UserNotFound(Exception):
    """
        Raise an error when doesn't a custom key
    """
    def _init_(self, message: str, identifier: str):
        Exception._init_(self, message)
        self.identifier: str = identifier
