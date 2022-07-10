from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint, DateTime, Boolean
from sqlalchemy.orm import relationship

from SuppleTime.pr.app.database import Base

from SuppleTime.pr.app.models.user import User

class Workspaces(Base):
    __tablename__ = "workspaces"
    
    id = Column(Integer, primary_key = True, autoincrement = True, unique=True)
    name = Column(String(120))
    ownerid = Column(Integer, ForeignKey(User.id), primary_key = True) #This should be foreign_key to user.id

    #tracked_tasks = relationship("Tracked_tasks")
    
    
class Tracked_tasks(Base):
    __tablename__ = "tracked_tasks"
    
    id = Column(Integer, primary_key = True, autoincrement = True, unique=True)
    #workspace_id = Column(Integer, ForeignKey(Workspaces.id)) #Foreign to Workspaces.id
    name = Column(String(120))
    date_one = Column(DateTime)
    date_two = Column(DateTime)
    tracked_user_id = Column(Integer, ForeignKey(User.id))
    planned_task_id = Column(Integer) #Foreign to planned_tasks.id
    billable = Column(Boolean)
    
    
class Trackers(Base):
    __tablename__ = "trackers"
    
    user_id = Column(Integer, ForeignKey(User.id), primary_key = True, unique=True) #Foreign to Users.id
    state = Column(String(16)) #e.g. none, track, pause
    pause_time = Column(Integer) #time in seconds
    pause_start_time = Column(DateTime)
    start_time = Column(DateTime)
