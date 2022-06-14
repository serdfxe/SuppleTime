from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base

import pr.app.config as conf


engine = create_engine(conf.DATABASE_URL)
Base = declarative_base(bind=engine)
