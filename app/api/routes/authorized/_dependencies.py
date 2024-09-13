from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from app import auth_service, settings
from app.database import session
from app.database.models import User
from app.errors import NotFoundUserInDatabase, OnlySuperuserRules
from app.schemas import TokenDataSchema, UserRoleEnum


UserTokenDataDepends = Depends(auth_service.bearer_authorisation)
TokenData = Annotated[TokenDataSchema, UserTokenDataDepends]


def get_current_user(
    token_data: TokenDataSchema = UserTokenDataDepends,
):
    stmt = select(User).where(User.username == token_data.username)
    user = session.scalars(stmt).first()

    if not user:
        raise NotFoundUserInDatabase(user.username)
    return user


CurrentUserDepends = Depends(get_current_user)
CurrentUser = Annotated[User, CurrentUserDepends]


def is_admin(token_data: TokenDataSchema = UserTokenDataDepends):
    if not token_data.role == UserRoleEnum.ADMIN:
        raise ValueError("U r not admin")


def is_supervisor(token_data: TokenDataSchema = UserTokenDataDepends):
    if not (
        (token_data.role == UserRoleEnum.SUPERVISOR)
        or (token_data.role == UserRoleEnum.ADMIN)
    ):
        raise ValueError("U r not supervisor")


def validate_superuser(username: str) -> None:
    if username != settings.super_user.username:
        OnlySuperuserRules


def validate_rules(
    current_role: UserRoleEnum, edit_role: UserRoleEnum
) -> None:
    if current_role <= edit_role:
        raise Exception("Not valid rules.")


AdminRules = Depends(is_admin)
SupervisorRules = Depends(is_supervisor)
