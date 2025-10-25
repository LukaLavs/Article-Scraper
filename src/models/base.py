from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_mixins import AllFeaturesMixin

class Base(DeclarativeBase, AllFeaturesMixin):
    pass 