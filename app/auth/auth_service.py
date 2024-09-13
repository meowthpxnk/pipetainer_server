import uuid

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from app import redis, settings
from app.database.models import User
from app.errors import (
    FailedRefreshSession,
    NotFoundSession,
    NotValidSession,
    NotValidTokenType,
)
from app.schemas import (
    JWTTokenTypeEnum,
    TokenDataSchema,
    TokenPayloadSchema,
    UserRoleEnum,
)

from .jwt_service import AuthJWTService


class AuthService:
    sessions_f = "userSession.{USERNAME}."
    current_session_f = sessions_f + "{SESSION_UUID}"

    def __init__(self):
        self.jwt_service = AuthJWTService()

    def bearer_authorisation(
        self,
        http_bearer: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ):
        try:
            data = self.jwt_service.decode(http_bearer.credentials)
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            self.validate_session(data.username, data.session_id)
        except NotValidSession:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not valid token session.",
            )
        return data

    def validate_session(self, username: str, session_id: str) -> None:
        try:
            self.get_session_token(username, session_id)
        except NotFoundSession:
            raise NotValidSession(username, session_id)

    def get_sessions(self, username: str) -> list[str]:
        return [redis.get(key) for key in self.get_session_keys(username)]

    def get_session_keys(self, username: str) -> list[str]:
        keys = redis.keys(self.sessions_f.format(USERNAME=username) + "*")
        return keys

    def close_sessions(
        self, username: str, exclude_session_id: str = None
    ) -> None:
        keys = self.get_session_keys(username)

        print(exclude_session_id)
        print(keys)
        print(list(filter(lambda key: key != exclude_session_id, keys)))

        if exclude_session_id:
            exclude_session_key = self.current_session_f.format(
                USERNAME=username, SESSION_UUID=exclude_session_id
            ).encode()

            keys = list(filter(lambda key: key != exclude_session_key, keys))

        for key in keys:
            redis.delete(key)

    def get_session_data(self, token: bytes) -> TokenDataSchema:
        return self.jwt_service.decode(token)

    def create_session(
        self, username: str, role: UserRoleEnum, session_id: str = None
    ) -> tuple[str, str]:

        if session_id == None:
            previous_sessions = self.get_sessions(username)

            if len(previous_sessions) >= settings.jwt.max_user_sessions:
                previous_sessions = [
                    self.get_session_data(key) for key in previous_sessions
                ]
                previous_sessions.sort(key=lambda session: session.exp)

                session_to_close = previous_sessions[0]

                self.close_session(
                    session_to_close.username, session_to_close.session_id
                )

            session_id = str(uuid.uuid4())

        access_token, refresh_token = self.jwt_service.encode(
            payload=TokenPayloadSchema(
                username=username,
                session_id=session_id,
                role=role,
            )
        )
        redis.set(
            self.current_session_f.format(
                USERNAME=username, SESSION_UUID=session_id
            ),
            refresh_token,
            settings.jwt.refresh_ttl,
        )

        return access_token, refresh_token

    def refresh_session(self, refresh_token: bytes) -> tuple[str, str]:
        data = self.jwt_service.decode(refresh_token)

        if not data.type == JWTTokenTypeEnum.REFRESH:
            raise NotValidTokenType(data.type, JWTTokenTypeEnum.REFRESH)

        session_token = self.get_session_token(data.username, data.session_id)

        if not session_token == refresh_token:
            self.close_session(data.username, data.session_id)
            raise FailedRefreshSession

        access_token, refresh_token = self.create_session(
            data.username, data.role, data.session_id
        )

        return access_token, refresh_token

    def get_session_token(self, username: str, session_id: str) -> str:
        token = redis.get(
            self.current_session_f.format(
                USERNAME=username, SESSION_UUID=session_id
            )
        )
        if token == None:
            raise NotFoundSession(username, session_id)
        return token

    def close_session(self, username: str, session_id: str) -> None:
        redis.delete(
            self.current_session_f.format(
                USERNAME=username, SESSION_UUID=session_id
            )
        )
