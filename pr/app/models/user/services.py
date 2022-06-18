import re
import secrets
import hashlib

from dependency_injector.wiring import inject, Provide
from SuppleTime.pr.app.containers import Container

from SuppleTime.pr.app.database.unit_of_work import UnitOfWork
from SuppleTime.pr.app.database.repository import Repository
from SuppleTime.pr.app.database.exceptions import NotFoundException

from SuppleTime.pr.app.models.user import User, ConfirmUser

from SuppleTime.pr.app.config import salt


@inject
def get_all_users(repository: Repository = Provide[Container.users_repository]) -> list:
    return repository.list()


@inject
def get_user(id: int, repository: Repository = Provide[Container.users_repository]) -> None or User:
    try:
        return repository.get(id=id)
    except NotFoundException as exc:
        print("User not found: ", exc)
        return None


def generate_token():
    return secrets.token_urlsafe()


def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

@inject
def create_user(name: str, email: str, password: str, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        user_id = len(get_all_users())
        new_user = User(name=name, email=email, id=user_id)
        new_confirm_user = ConfirmUser(id=user_id, token=generate_token(), password_hash=get_password_hash(password))
        uow.repository.save(new_user)
        uow.repository.save(new_confirm_user)
        uow.commit()
        return "Success"


def is_valid_email(email: str) -> bool: 
    return re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email)


def is_valid_password(password: str) -> bool:
    if len(password) < 8:
        return "Make sure your password is at lest 8 letters"
    elif re.search('[0-9]',password) is None:
        return "Make sure your password has a number in it"
    elif re.search('[A-Z]',password) is None: 
        return "Make sure your password has a capital letter in it"
    else:
        return True


def register_user(data) -> str:
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if name is None and email is None: return "No data"
    if name == '' or name.count(' '): return "Incorrect name"
    if email == '' or not is_valid_email(email): return "Incorrect email"
    is_valid = is_valid_password(password)
    if is_valid is not True: return is_valid
    return create_user(name, email, password)


@inject
def delete_all_users(unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        #users = get_all_users()
        uow.repository.session.query(ConfirmUser).delete()
        uow.repository.session.query(User).delete()
        
        uow.commit()
