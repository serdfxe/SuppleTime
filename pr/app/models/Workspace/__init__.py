from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint, DateTime, Boolean, BigInteger, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from SuppleTime.pr.app.database import Base

from SuppleTime.pr.app.models.user import User

class Workspaces(Base):
    __tablename__ = "workspaces"
    
    id = Column(Integer, primary_key = True, autoincrement = True, unique=True)
    name = Column(String(120))
    ownerid = Column(Integer, ForeignKey(User.id), unique = True) #This should be foreign_key to user.id

    # tracked_tasks = relationship("Tracked_tasks")
    # tags = relationship("Tags")
    # workspaces_members = relationship("Workspaces_members")
    
    
class Workspaces_members(Base):
    __tablename__ = "workspaces_members"
    
    workspace_id = Column(Integer, ForeignKey(Workspaces.id), primary_key = True)
    user_id = Column(Integer, ForeignKey(User.id), primary_key = True)####
    role = Column(String(120))
    
    
    
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
    pause_time = Column(Integer) #time in seconds
    
    tracked_tasks_tags = relationship("Tracked_tasks_tags")
    
    
class Tracked_tasks_tags(Base):
     __tablename__ = "tracked_tasks_tags"
    
     tag_id = Column(BigInteger, ForeignKey("tags.id"))
     tracked_tasks_id = Column(Integer, ForeignKey(Tracked_tasks.id), primary_key = True)
    
    
class Trackers(Base):
    __tablename__ = "trackers"
    
    user_id = Column(Integer, ForeignKey(User.id), primary_key = True, unique=True) #Foreign to Users.id
    state = Column(String(16)) #e.g. none, track, pause
    pause_time = Column(Integer) #time in seconds
    pause_start_time = Column(DateTime)
    start_time = Column(DateTime)
    billable = Column(Boolean)
    name = Column(String(120))
    
    
class Trackers_tags(Base):
    __tablename__ = "trackers_tags"


    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id))
    tag_id = Column(BigInteger, ForeignKey("tags.id"))

    tags = relationship("Tags")
    
    
class Tags(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key = True, autoincrement = True, unique = True)
    workspace_id = Column(Integer, ForeignKey(Workspaces.id))
    name = Column(String(120))
    color = Column(String(30))

    tracked_tasks_tags = relationship("Tracked_tasks_tags")
    trackers_tags = relationship("Trackers_tags")
    
    
