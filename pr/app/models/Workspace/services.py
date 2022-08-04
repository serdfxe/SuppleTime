from datetime import date, datetime, timedelta

from random import randint

from dependency_injector.wiring import inject, Provide
from SuppleTime.pr.app.containers import Container

from SuppleTime.pr.app.database.unit_of_work import UnitOfWork
from SuppleTime.pr.app.database.repository import Repository

from SuppleTime.pr.app.models.Workspace import *

from SuppleTime.pr.app.config import *



@inject
def create_workspace(user_id: int, name="default", unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    """Create workspace for user by id after registration"""
    with unit_of_work as uow:
        workspace = Workspaces(ownerid=user_id, name=name)
        uow.repository.save(workspace)
        uow.commit()
        uow.repository.session.refresh(workspace)
        uow.repository.session.expunge(workspace)

        ws_m = Workspaces_members(workspace_id=workspace.id, user_id=user_id, role="owner")
        uow.repository.save(ws_m)

        uow.commit()


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
    if task_id or task_id==0:
        with unit_of_work as uow:
            uow.repository.session.query(Tracked_tasks).filter_by(id=task_id).delete()
            uow.commit()
            return "Success", "success"
    return "Error", "error"


@inject
def is_user_in_ws(user_id: int, workspace_id: int, repository: Repository = Provide[Container.users_repository]) -> bool:
    member = repository.session.query(Workspaces_members).filter_by(user_id=user_id, workspace_id=workspace_id).first()
    return True if member else False


@inject
def get_users_default_ws(user_id: int, repository: Repository = Provide[Container.users_repository]) -> int:
    ws = repository.session.query(Workspaces).filter_by(ownerid=user_id, name="default").first()
    return ws


@inject
def create_tag(workspace_id: int, name: str, uow: UnitOfWork = Provide[Container.user_uow]) -> bool:
    with uow:
        tag = Tags(workspace_id=workspace_id, name=name, color="119 128 255")
        uow.repository.save(tag)

        uow.commit()

        return True


@inject
def add_tag_to_tracker(user_id: int, tag_id: int, uow: UnitOfWork = Provide[Container.user_uow]) -> bool:
    with uow:
        rep = uow.repository.session

        tag = rep.query(Tags).filter_by(id=tag_id).first()
        if not tag: return False

        member = Trackers_tags(user_id=user_id, tag_id=tag.id)
        uow.repository.save(member)

        uow.commit()

        return True


@inject
def get_all_trackers_tags(user_id: int, repository: Repository = Provide[Container.users_repository]):
    rep = repository.session
    l = rep.query(Trackers_tags).filter_by(user_id=user_id).all()

    return [{"name": i.tags.name, "color": [int(j) for j in i.tags.color.split(" ")]} for i in l] 


@inject
def get_all_ws_tags(workspace_id: int, repository: Repository = Provide[Container.users_repository]):
    rep = repository.session
    l = rep.query(Tags).filter_by(workspace_id=workspace_id).all()

    return [{"name": i.name, "color": [int(j) for j in i.color.split(" ")]} for i in l] 


def get_all_users_tags(user_id: int):
    return get_all_ws_tags(get_users_default_ws(user_id).id)


# @inject
# def post_tracked_task(data, tracked_user_id, repository: Repository = Provide[Container.users_repository]):
#     name = data.get("name")
#     time = data.get("time")

#     tracker = repository.session.query(Trackers).filter_by(user_id=tracked_user_id).first()
#     start_time = trac


#--------------------- Временно ---------------------#

def get_list_colors(color):
    return (color,  [i - 16 for i in color], [i - 26 for i in color])

def rand_color():
    return color_list[randint(0, len(color_list) - 1)]

#--------------------- Временно ---------------------#


@inject
def post_task(data, tracked_user_id, repository: Repository = Provide[Container.users_repository]):
    """Make task from post form"""

    name = data.get("name")

    date_one = data.get("date_one")
    date_two = data.get("date_two")

    now = datetime.now()

    if not date_one or not date_two: return "Invalid inputs", "error"
    date_one = date_one.split(":")
    if not name: name = ''

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

    billable = tracker = repository.session.query(Trackers).filter_by(user_id=tracked_user_id).first().billable
    
    if data.get("date") and data.get("date") != '':
        y, m, d = data.get("date").split("-")
        y = int(y)
        d = int(d)
        m = int(m)
        date_one = date_one.replace(day=d, year=y, month=m)
        date_two = date_two.replace(day=d, year=y, month=m)

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
    time = f"{hours}:{minutes}"
    if time == "0:00": return "<1 мин"
    return time


@inject
def get_tags_by_task_id(id: int,  repository: Repository = Provide[Container.users_repository]):
    return {"Тег 1": rand_color(), "Тег 2": rand_color()}


@inject
def get_all_users_tasks_by_date(user_id: int, date: datetime, repository: Repository = Provide[Container.users_repository]):
    start = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    l = repository.session.query(Tracked_tasks).filter(Tracked_tasks.tracked_user_id == user_id, Tracked_tasks.date_one >= start, Tracked_tasks.date_one <= end).all()
    # l = [(i.name, i.billable, i.date_one.strftime("%H:%M"), i.date_two.strftime("%H:%M"), get_differ_time_with_sec(i.date_one, i.date_two, i.pause_time), i.id) for i in l]
    tasks = []
    for i in l: 
        tasks.append(
            {
                "name": i.name,
                "bill": i.billable, 
                "from": i.date_one.strftime("%H:%M"), 
                "to": i.date_two.strftime("%H:%M"), 
                "time": get_differ_time_with_sec(i.date_one, i.date_two, i.pause_time), 
                "id": i.id,
                "tags": get_tags_by_task_id(i.id),
            }
        )
    return tasks


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
def start_tracker(user_id: int, name = None, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
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
def change_billable(user_id:int, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        tracker = uow.repository.session.query(Trackers).filter_by(user_id=user_id).first()
        tracker.billable = not tracker.billable

        uow.commit()


@inject
def get_tracker_state(user_id: int, repository: Repository = Provide[Container.users_repository]):
    tracker = repository.session.query(Trackers).filter_by(user_id=user_id).first()
    if tracker:
        if tracker.state == "none":
            return {"state": "none", "name": "", "bill": tracker.billable, "tags": get_all_trackers_tags(user_id)}
        elif tracker.state == "track":
            return {
                "state": tracker.state,
                "hour": tracker.start_time.hour,
                "second": tracker.start_time.second + tracker.pause_time,
                "minute": tracker.start_time.minute,
                "name": tracker.name,
                "bill": tracker.billable, 
                "tags": get_all_trackers_tags(user_id)
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
                "bill": tracker.billable,
                "tags": get_all_trackers_tags(user_id)
            }
        #return {"state": tracker.state, "start_time": tracker.start_time, "name": tracker.name, "billable": tracker.billable, "time": get_time_by_start_and pause}

