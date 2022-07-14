from datetime import date, datetime

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
    """Create task"""
    with unit_of_work as uow:
        task = Tracked_tasks(name=name, date_one=date_one, date_two=date_two, tracked_user_id=tracked_user_id, planned_task_id=planned_task_id, billable=billable)
        uow.repository.save(task)

        uow.commit()


def post_task(data, tracked_user_id):
    """Make task from post form"""

    name = data.get("name")

    date_one = data.get("date_one")
    date_two = data.get("date_two")
    
    billable = True if data.get("billable") else False

    now = datetime.now()

    if not date_one or not date_two or not name: return "Invalid inputs", "error"
    date_one = date_one.split(":")

    try:
        date_one = now.replace(hour=int(date_one[0]), minute=int(date_one[1]))
    except Exception as ex:
        return "Error", "error"
    
    date_two = date_two.split(":")

    try:
        date_two = now.replace(hour=int(date_two[0]), minute=int(date_two[1]))
    except Exception as ex:
            return "Error", "error"
        
    if date_one >= date_two: return "Invalid time", "error"
    
    create_task(name, date_one, date_two, tracked_user_id, billable)

    return "Success", "success"


@inject
def get_all_users_tasks(user_id: int, repository: Repository = Provide[Container.users_repository]):
    return repository.session.query(Tracked_tasks).filter_by(tracked_user_id=user_id).all()
