from sqlalchemy.orm import relationship

from db.models.base import BaseModel
from sqlalchemy import Column, String, Integer, Float


class SpyCat(BaseModel):
    name = Column(String, nullable=False)
    exp_years = Column(Integer)
    breed = Column(String, nullable=False)
    salary = Column(Float)

    # Relations
    missions = relationship("Mission", back_populates="spy_cat")
