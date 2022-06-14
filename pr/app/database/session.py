from sqlalchemy.orm import sessionmaker
from pr.app.database import engine


Session = sessionmaker(bind=engine)
