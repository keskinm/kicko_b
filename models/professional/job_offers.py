from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.base import Base
from models.associations.associations import job_offer_candidate_association
from models.professional.professional import Professional


class JobOffers(Base):
    __tablename__ = "job_offers"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    description = Column(String)
    requires = Column(String)

    business_id = Column(Integer, ForeignKey(Professional.id))

    candidate = relationship(
        "Candidate",
        secondary=job_offer_candidate_association,
        back_populates="job_offers",
    )

    def __init__(self, name, description, requires, business_id):
        self.name = name
        self.description = description
        self.requires = requires
        self.business_id = business_id
