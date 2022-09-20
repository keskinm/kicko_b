from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from engine.engine import MAIN_ENGINE

from tables.professional.professional import Professional

Base = declarative_base()


class Business(Base):
    __tablename__ = "business"

    id = Column(Integer, primary_key=True, unique=True)
    professional_id = Column(Integer, ForeignKey(Professional.id))
    email = Column(String(100), unique=True)
    name = Column(String(100))
    country = Column(String)
    city = Column(String)
    phone_number = Column(String)
    image_id = Column(String)

    def __init__(
        self,
        professional_id,
        name=None,
        email=None,
        country=None,
        city=None,
        phone_number=None,
        image_id=None,
    ):
        self.name = name
        self.professional_id = professional_id
        self.email = email
        self.country = country
        self.city = city
        self.phone_number = phone_number
        self.image_id = image_id


Base.metadata.create_all(MAIN_ENGINE)
