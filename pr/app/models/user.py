from sqlalchemy import Column, String, Integer

from pr.app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    email = Column(String(120))
