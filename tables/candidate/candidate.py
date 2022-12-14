import enum

from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from engine.base import Base
from engine.engine import MAIN_ENGINE
from tables.associations.associations import job_offer_candidate_association

candidate_syntax = {
    "french": {
        "sex": ["", "Homme", "Femme", "Non genré"],
        "study_level": ["", "Licence", "Master"],
    }
}


class Sex(enum.Enum):
    null = 0
    male = 1
    female = 2
    non_binary = 3


class StudyLevel(enum.Enum):
    null = 0
    bachelor_degree = 1
    master_degree = 2


enums_to_module = {"sex": Sex, "study_level": StudyLevel}


class Candidate(Base):
    __tablename__ = "candidate"

    id = Column(Integer, primary_key=True, unique=True)
    firebase_id = Column(String, unique=True)
    username = Column(String)
    password = Column(String)
    email = Column(String(100), unique=True)
    country = Column(String)
    zone = Column(String)
    phone_number = Column(String)
    study_level = Column(Enum(StudyLevel))
    l_study_level = Column(String)
    sex = Column(Enum(Sex))
    l_sex = Column(String)
    language = Column(String)

    image_id = Column(String)
    resume_id = Column(String)

    job_offers = relationship(
        "JobOffers",
        secondary=job_offer_candidate_association,
        back_populates="candidate",
    )

    def __init__(
        self,
        firebase_id,
        username,
        password,
        email,
        country=None,
        zone=None,
        phone_number=None,
        study_level=StudyLevel.null,
        l_study_level="",
        sex=Sex.null,
        l_sex="",
        language="french",
        image_id=None,
        resume_id=None
    ):
        self.firebase_id = firebase_id
        self.username = username
        self.password = password
        self.email = email
        self.country = country
        self.zone = zone
        self.phone_number = phone_number

        self.study_level = study_level
        self.l_study_level = l_study_level

        self.sex = sex
        self.l_sex = l_sex

        self.language = language

        self.image_id = image_id
        self.resume_id = resume_id


def create():
    Base.metadata.create_all(MAIN_ENGINE)
