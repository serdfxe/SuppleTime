from dependency_injector.wiring import inject, Provide
from app.containers import Container

from app.database.unit_of_work import UnitOfWork


@inject
def get_all_users(unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    print(unit_of_work.session)


def get_user(id: int):
    return 'user'


def create_user():
    pass 
