from datetime import datetime

from dependency_injector.wiring import inject, Provide
from SuppleTime.pr.app.containers import Container

from SuppleTime.pr.app.database.unit_of_work import UnitOfWork
from SuppleTime.pr.app.database.repository import Repository

from SuppleTime.pr.app.models.Workspace import *


@inject
def create_workspace(user_id: int, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    """Create workspace for user by id after registration"""
    pass


@inject
def create_tracker(user_id: int, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    """Create tracker for user by id after registration"""
    with unit_of_work as uow:
        tracker = Trackers(user_id=user_id, state="none", pause_time=0, pause_start_time=None, start_time=None)
        uow.repository.save(tracker)

        uow.commit()


@inject
def create_task(name: str, date_one: datetime, date_two: datetime, tracked_user_id: int, billable: bool, planned_task_id=None, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        task = Tracked_tasks(name=name, date_one=date_one, date_two=date_two, tracked_user_id=tracked_user_id, planned_task_id=planned_task_id, billable=billable)
        uow.repository.save(task)

        uow.commit()
        