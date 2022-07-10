from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from flask_login import UserMixin

from SuppleTime.pr.app.database import Base


class User(UserMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(120))
    email = Column(String(120), primary_key=True)

    confirm_users = relationship("ConfirmUser", back_populates="users", uselist=False)
    workspaces = relationship("Workspaces")
    trackers = relationship("Trackers")


class ConfirmUser(Base):
    __tablename__ = 'confirm_users'

    id = Column(Integer, ForeignKey(User.id), primary_key=True, unique=True)
    token = Column(String(120), primary_key=True)
    password_hash = Column(String(120))

    users = relationship("User", back_populates="confirm_users")


class NonConfirmedUser(Base):
    __tablename__ = 'non_comfirm_users'

    id = Column(Integer, primary_key=True, unique=True)
    email = Column(String(120), primary_key=True)
    password_hash = Column(String(120))
    confirm_token = Column(String(120), unique=True)

'''
class Anonymous(AnonymousUserMixin):

    def __init__(self):
        pass


    def is_authenticated(self):
        return True
'''