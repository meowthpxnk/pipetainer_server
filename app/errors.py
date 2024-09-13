from sqlalchemy.sql._typing import _ColumnExpressionArgument

from app.schemas import JWTTokenTypeEnum


class OnlySuperuserRules(Exception):
    def __init__(self) -> None:
        super().__init__(f"Only superuser rules")


class AlreadyExistsInDB(Exception):
    def __init__(
        self, whereclause: _ColumnExpressionArgument[bool], class_name: str
    ):
        print(whereclause[0])
        super().__init__(
            f"Already exists {class_name} item in database where ({whereclause})"
        )


class UserAlreadyExist(Exception):
    def __init__(self, username) -> None:
        super().__init__(f'User with username "{username}", already exist')


class ServerAlreadyExist(Exception):
    def __init__(self, short_name) -> None:
        super().__init__(
            f'Server with short_name "{short_name}", already exist'
        )


class ApiKeyAlreadyexist(Exception):
    def __init__(self, name) -> None:
        super().__init__(f'ApiKey with name "{name}", already exist')


class SuperuserAlreadyExist(UserAlreadyExist):
    def __init__(self, username) -> None:
        super().__init__(
            f'Superuser with username "{username}", already exist'
        )


class WrongPassword(Exception):
    def __init__(self) -> None:
        super().__init__("Wrong password")


class WrongPasswordOrUsername(Exception):
    def __init__(self) -> None:
        super().__init__("Wrong password or username.")


class NotValidTokenType(Exception):
    def __init__(
        self, current_type: JWTTokenTypeEnum, expected_type: JWTTokenTypeEnum
    ) -> None:
        super().__init__(
            f"Not valid token type, current type is {current_type}, but expected is {expected_type}"
        )


class FailedRefreshSession(Exception):
    def __init__(self) -> None:
        super().__init__("Failed refresh session.")


class NotFoundSession(Exception):
    def __init__(self, username, session_id) -> None:
        super().__init__(
            f"Not found session with username {username} id {session_id}, in session storage."
        )


class NotFoundUserInDatabase(Exception):
    def __init__(self, username) -> None:
        super().__init__(f'Not found user "{username}" in database.')


class NotFoundInDB(Exception):
    def __init__(
        self, whereclause: _ColumnExpressionArgument[bool], class_name: str
    ):
        super().__init__(
            f"Not found {class_name} in database where ({whereclause})"
        )


class NotFoundAnySession(Exception):
    def __init__(self, username) -> None:
        super().__init__(
            f"Not found any sessions with username {username}, in session storage."
        )


class NotValidSession(Exception):
    def __init__(self, username, session_id) -> None:
        super().__init__(
            f"Not valid session with username {username} id {session_id}."
        )


class NotExistImage(Exception):
    def __init__(self, image_name) -> None:
        super().__init__(
            f"Image with name {image_name} not existed in registry."
        )


class NotExistDevice(Exception):
    def __init__(self, device_name) -> None:
        super().__init__(
            f"Device with name {device_name} not existed in docker."
        )
