from fastapi import APIRouter

from app import auth_service
from app.schemas import FetchPayloadSchema, User

from ._dependencies import TokenData


session_routes = APIRouter()


@session_routes.patch("/sessions-close")
async def close_session(token_data: TokenData):
    auth_service.close_sessions(
        token_data.username, exclude_session_id=token_data.session_id
    )


@session_routes.patch("/logout")
async def logout(token_data: TokenData):
    auth_service.close_session(token_data.username, token_data.session_id)


@session_routes.get("/get_payload")
async def get_payload(token_data: TokenData):
    return FetchPayloadSchema(
        username=token_data.username, role=token_data.role
    )
