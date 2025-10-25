from sqlalchemy import create_engine
from .config import settings
from sqlalchemy.orm import Session

engine = create_engine(settings.database_url, echo=True)

session = Session(engine)
