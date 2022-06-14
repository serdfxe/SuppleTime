from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base

import app.config as conf


engine = create_engine(conf.DATABASE_URL)
Base = declarative_base(bind=engine)
