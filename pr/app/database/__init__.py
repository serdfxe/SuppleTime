from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import SuppleTime.pr.app.config as conf


engine = create_engine(conf.DATABASE_URL)
Base = declarative_base(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()
Base.metadata.create_all()
session.commit()