from fastapi import APIRouter, HTTPException, Request, Response, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select

from app import auth_service, settings
from app.auth.utils import check_password
from app.database import session
from app.database.models import User
from app.errors import (
    FailedRefreshSession,
    NotFoundSession,
    WrongPassword,
    WrongPasswordOrUsername,
)
from app.schemas import AuthForm


auth_router = APIRouter()


@auth_router.post(
    "/authorisate",
)
async def authorisate(form: AuthForm, response: Response):
    stmt = select(User).where(User.username == form.username)
    user = session.scalars(stmt).first()
    if not user:
        raise WrongPasswordOrUsername

    password_hash = user.password_hash
    try:
        check_password(form.password, password_hash)
    except WrongPassword:
        raise WrongPasswordOrUsername
    access_token, refresh_token = auth_service.create_session(
        user.username, user.role
    )

    response.set_cookie(
        "Refresh-Token",
        refresh_token,
        max_age=settings.jwt.refresh_ttl,
        expires=settings.jwt.refresh_ttl,
        samesite="none",
        secure=True,
        httponly=True,
        path="/refresh-session",
    )

    return {"Access-Token": access_token}


@auth_router.post("/refresh-session")
async def refresh_session(response: Response, request: Request):

    BAD_TOKEN = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not valid refresh token.",
        headers={
            "set-cookie": "Refresh-Token=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/refresh-session"
        },
    )

    token = request.cookies.get("Refresh-Token")
    if not token:
        raise BAD_TOKEN
    try:
        access_token, refresh_token = auth_service.refresh_session(
            token.encode()
        )
    except (InvalidTokenError, NotFoundSession, FailedRefreshSession):
        raise BAD_TOKEN

    response.set_cookie(
        "Refresh-Token",
        refresh_token,
        max_age=settings.jwt.refresh_ttl,
        expires=settings.jwt.refresh_ttl,
        samesite="none",
        secure=True,
        httponly=True,
        path="/refresh-session",
    )

    return {"Access-Token": access_token}
