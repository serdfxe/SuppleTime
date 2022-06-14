from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory

from app.database.unit_of_work import AlchemyUnitOfWork
from app.models.repository import UserRepository
from app.database.session import Session


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        packages=[
            "app.models",
        ]
    )

    session_creator = Factory(
        Session
    )

    users_repository = Factory(
        UserRepository,
        session=session_creator
    )

    user_uow = Factory(
        AlchemyUnitOfWork,
        repository=users_repository,
    )
