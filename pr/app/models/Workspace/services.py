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


@inject # !!!!!!!!!!!!!!!!!!!!дописать пауз тайм
def create_task(name: str, date_one: datetime, date_two: datetime, tracked_user_id: int, billable: bool, pause_time=0, planned_task_id=None, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    """Create task"""
    with unit_of_work as uow:
        task = Tracked_tasks(name=name, date_one=date_one, date_two=date_two, tracked_user_id=tracked_user_id, planned_task_id=planned_task_id, billable=billable, pause_time=0)
        uow.repository.save(task)

        uow.commit()


@inject
def delete_task(task_id: int, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    """Delelete task by id"""
    if task_id:
        with unit_of_work as uow:
            uow.repository.session.query(Tracked_tasks).filter_by(id=task_id).delete()
            uow.commit()
            return "Success", "success"
    return "Error", "error"


# @inject
# def post_tracked_task(data, tracked_user_id, repository: Repository = Provide[Container.users_repository]):
#     name = data.get("name")
#     time = data.get("time")

#     tracker = repository.session.query(Trackers).filter_by(user_id=tracked_user_id).first()
#     start_time = trac


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


def get_differ_time_with_sec(t1: datetime, t2: datetime, sec: int) -> str:
    if t1 >= t2:
        delta = t1 - t2 
        delta = delta.seconds - sec
    else:
        delta = t2 - t1
        delta = delta.seconds - sec
    hours = delta // 3600
    minutes = str(delta // 60 - hours*60)
    if len(minutes) == 1: minutes = "0"+minutes
    return f"{hours}:{minutes}"


@inject
def get_all_users_tasks_by_date(user_id: int, date: datetime, repository: Repository = Provide[Container.users_repository]):
    start = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start.replace(day=start.day+1)
    l = repository.session.query(Tracked_tasks).filter(Tracked_tasks.tracked_user_id == user_id, Tracked_tasks.date_one >= start, Tracked_tasks.date_one <= end).all()
    l = [(i.name, i.billable, i.date_one.strftime("%H:%M"), i.date_two.strftime("%H:%M"), get_differ_time_with_sec(i.date_one, i.date_two, i.pause_time), i.id) for i in l]
    return l


@inject
def delete_all_users_tasks(user_id: int, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        uow.repository.session.query(Tracked_tasks).filter_by(tracked_user_id=user_id).delete()
        uow.commit()


def get_differ_time(t1: datetime, t2: datetime) -> str:
    if t1 >= t2:
        delta = t1 - t2
    else:
        delta = t2 - t1
    hours = delta.seconds // 3600
    minutes = str(delta.seconds // 60 - hours*60)
    if len(minutes) == 1: minutes = "0"+minutes
    return f"{hours}:{minutes}"
    

@inject
def start_tracker(user_id: int, name = None, billable = False, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        tracker = uow.repository.session.query(Trackers).filter_by(user_id=user_id).first()
    if tracker.state == "none":
        with unit_of_work as uow:
            tracker = uow.repository.session.query(Trackers).filter_by(user_id=user_id).first()
            tracker.name = name
            tracker.state = "track"
            tracker.pause_time = 0
            tracker.pause_start_time = None
            tracker.start_time = datetime.now()
            tracker.billable = billable
            
            uow.commit()
        return None
    if tracker.state == "pause":
        with unit_of_work as uow:
            tracker = uow.repository.session.query(Trackers).filter_by(user_id=user_id).first()
            tracker.state = "track"
            delta = datetime.now() - tracker.pause_start_time
            tracker.pause_time += delta.seconds
            
            uow.commit()
        return None 
        

@inject
def pause_tracker(user_id: int, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        tracker = uow.repository.session.query(Trackers).filter_by(user_id=user_id).first()
    if True:
        with unit_of_work as uow:
            tracker = uow.repository.session.query(Trackers).filter_by(user_id=user_id).first()
            tracker.state = "pause"
            tracker.pause_start_time = datetime.now()
    
            uow.commit()
    return None
    

@inject
def stop_tracker(user_id:int, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        tracker = uow.repository.session.query(Trackers).filter_by(user_id=user_id).first()
        tracker.state = "none"
        name = tracker.name
        date_one = tracker.start_time
        date_two = datetime.now()
        tracked_user_id = user_id
        billable = tracker.billable
        pause_time = tracker.pause_time

        uow.commit()
    return create_task(name, date_one, date_two, tracked_user_id, billable, pause_time)


@inject
def get_tracker_state(user_id: int, repository: Repository = Provide[Container.users_repository]):
    tracker = repository.session.query(Trackers).filter_by(user_id=user_id).first()
    if tracker:
        if tracker.state == "none":
            return {"state": "none", "name": ""}
        elif tracker.state == "track":
            return {
                "state": tracker.state, 
                "start_time": tracker.start_time,
                "name": tracker.name,
                "billable": tracker.billable, 
                "pause_time": tracker.pause_time
            }
        elif tracker.state == "pause":
            time = tracker.pause_start_time - tracker.start_time
            time = time.seconds - tracker.pause_time
            h = time//3600
            m = time//60 - h*60
            s = time - m*60 - h*3600

            h = str(h)
            if len(h) == 1: h = "0" + h

            m = str(m)
            if len(m) == 1: m = "0" + m

            s = str(s)
            if len(s) == 1: s = "0" + s

            time = f"{h}:{m}:{s}"

            return {
                "state": tracker.state,
                "time": time,
                "name": tracker.name,
                "billable": tracker.billable
            }
        #return {"state": tracker.state, "start_time": tracker.start_time, "name": tracker.name, "billable": tracker.billable, "time": get_time_by_start_and pause}

