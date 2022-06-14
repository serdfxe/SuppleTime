from dependency_injector.wiring import inject, Provide
from pr.app.containers import Container

from pr.app.database.unit_of_work import UnitOfWork
from pr.app.database.repository import Repository
from pr.app.database.exceptions import NotFoundException
from pr.app.models.user import User


@inject
def get_all_users(repository: Repository = Provide[Container.users_repository]):
    return repository.list()


@inject
def get_user(id: int, repository: Repository = Provide[Container.users_repository]):
    try:
        return repository.get(id=id)
    except NotFoundException as exc:
        print("User not found: ", exc)
        return None


@inject
def create_user(name: str, email: str, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        new_user = User(name=name, email=email)
        print("New user created: " + new_user.name)
        uow.repository.save(new_user)
        uow.commit()
