from sqlalchemy.orm import sessionmaker
from SuppleTime.pr.app.database import engine


Session = sessionmaker(bind=engine)
