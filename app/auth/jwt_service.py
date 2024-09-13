import datetime

import jwt

from app import settings
from app.schemas import JWTTokenTypeEnum, TokenDataSchema, TokenPayloadSchema


class AuthJWTService:

    private_key: bytes
    public_key: bytes

    def __init__(self) -> None:
        self.access_ttl = settings.jwt.access_ttl
        self.refresh_ttl = settings.jwt.refresh_ttl
        self.algorithm = settings.jwt.algorithm

    def _set_keys(self):
        with open(settings.jwt.private_key_path, "rb") as f:
            self.private_key = f.read()

        with open(settings.jwt.public_key_path, "rb") as f:
            self.public_key = f.read()

    def encode(self, payload: TokenPayloadSchema) -> tuple[str, str]:
        now = datetime.datetime.now(datetime.UTC)

        access_payload = TokenDataSchema(
            **payload.model_dump(),
            type=JWTTokenTypeEnum.ACCESS,
            exp=jwt.api_jwt.timegm(
                (
                    now + datetime.timedelta(seconds=self.access_ttl)
                ).utctimetuple()
            ),
        ).model_dump(mode="json")

        access_token = jwt.encode(
            access_payload,
            key=self.private_key,
            algorithm=self.algorithm,
        )

        refresh_payload = TokenDataSchema(
            **payload.model_dump(),
            type=JWTTokenTypeEnum.REFRESH,
            exp=jwt.api_jwt.timegm(
                (
                    now + datetime.timedelta(seconds=self.refresh_ttl)
                ).utctimetuple()
            ),
        ).model_dump(mode="json")

        refresh_token = jwt.encode(
            refresh_payload,
            key=self.private_key,
            algorithm=self.algorithm,
        )

        return access_token, refresh_token

    def decode(self, token: str) -> TokenDataSchema:
        data = jwt.decode(token, self.public_key, algorithms=[self.algorithm])
        return TokenDataSchema(**data)
