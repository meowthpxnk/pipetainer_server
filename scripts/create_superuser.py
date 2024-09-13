import _base_script
from sqlalchemy import select

from app import logger, settings
from app.auth.utils import hash_password
from app.database import session
from app.database.models import User
from app.errors import SuperuserAlreadyExist
from app.schemas import CreateUserForm, UserRoleEnum


username = settings.super_user.username
password = settings.super_user.password


stmt = select(User).where(User.username == username)
user = session.scalars(stmt).first()

if user:
    raise SuperuserAlreadyExist(username)

form = CreateUserForm(
    username=username, password=password, role=UserRoleEnum.ADMIN
)


user = User(form)
user.create()

logger.info(f"Superuser {username} successful created")
