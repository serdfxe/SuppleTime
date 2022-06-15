from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory

from SuppleTime.pr.app.database.unit_of_work import AlchemyUnitOfWork
from SuppleTime.pr.app.models.repository import UserRepository
from SuppleTime.pr.app.database.session import Session


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        packages=[
            "SuppleTime.pr.app.models",
        ]
    )

    session_creator = Factory(
        Session
    )

    users_repository = Factory(
        UserRepository,
        session=session_creator,
    )

    user_uow = Factory(
        AlchemyUnitOfWork,
        repository=users_repository,
    )
