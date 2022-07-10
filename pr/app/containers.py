from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory

from SuppleTime.pr.app.database.unit_of_work import AlchemyUnitOfWork
from SuppleTime.pr.app.models.user.repository import UserRepository, NonConfirmedUserRepository, ConfirmUserRepository
from SuppleTime.pr.app.database.session import Session

from SuppleTime.pr.app.models.Workspace.repository import *


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

    confirm_users_repository = Factory(
        ConfirmUserRepository,
        session=session_creator,
    )

    nonconfirmed_users_repository = Factory(
        NonConfirmedUserRepository,
        session=session_creator,
    )

    workspaces_repository = Factory(
        WorkspacesRepository,
        session=session_creator,
    )

    tracked_tasks_repository = Factory(
        TrackedTasksRepository,
        session=session_creator,
    )
    
    trackers_repository = Factory(
        TrackersRepository,
        session=session_creator,
    )

    user_uow = Factory(
        AlchemyUnitOfWork,
        repository=users_repository,
    )
