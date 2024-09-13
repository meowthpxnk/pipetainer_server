from fastapi import APIRouter

from app import settings
from app.database.models import User
from app.schemas import CreateUserForm
from app.schemas import User as UserSchema

from ._dependencies import SupervisorRules, TokenData, validate_rules


user_routes = APIRouter(prefix="/user")


@user_routes.post("/create", dependencies=[SupervisorRules])
async def create_user(form: CreateUserForm, token_data: TokenData):

    is_superuser = token_data.username == settings.super_user.username

    if not is_superuser:
        validate_rules(token_data.role, form.role)

    User.exists(form.username)
    User(form).create()


@user_routes.get("/{username}", dependencies=[SupervisorRules])
async def get_user(username: str):
    user = User.select_where(User.username == username)
    return UserSchema(username=user.username, role=user.role)


@user_routes.delete("/{username}", dependencies=[SupervisorRules])
async def delete_user(username: str, token_data: TokenData):
    if username == token_data.username:
        raise Exception("Can't delete self.")

    if username == settings.super_user.username:
        raise Exception("Can't delete superuser.")

    user = User.select_where(User.username == username)

    is_superuser = token_data.username == settings.super_user.username

    if not is_superuser:
        validate_rules(token_data.role, user.role)

    user.delete()


@user_routes.get("", dependencies=[SupervisorRules])
async def get_users():
    return [
        UserSchema(username=user.username, role=user.role)
        for user in User.select_where(all=True)
    ]
