import re

from dependency_injector.wiring import inject, Provide
from SuppleTime.pr.app.containers import Container

from SuppleTime.pr.app.database.unit_of_work import UnitOfWork
from SuppleTime.pr.app.database.repository import Repository
from SuppleTime.pr.app.database.exceptions import NotFoundException

#from SuppleTime.pr.app.models.user import User


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


@inject
def create_user(name: str, email: str, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        new_user = User(name=name, email=email)
        uow.repository.save(new_user)
        uow.commit()
        return "Success"



def is_valid_email(email: str) -> bool: 
    return re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email)


def register_user(data) -> str:
    name = data.get("name")
    email = data.get("email")
    if name is None and email is None: return "No data"
    if name == '' or name.count(' '): return "Incorrect name"
    if email == '' or not is_valid_email(email): return "Incorrect email"
    return create_user(name, email)
