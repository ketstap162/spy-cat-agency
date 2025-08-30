from sqlalchemy.orm import relationship

from db.models.base import BaseModel
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey

from db.models.spy_cats import SpyCat


class Target(BaseModel):
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)

    # Relations
    notes = relationship("TargetNote", back_populates="target", cascade="all, delete-orphan")
    missions = relationship("Mission", back_populates="target", cascade="all, delete-orphan")


class TargetNote(BaseModel):
    note = Column(String, nullable=False)
    target_id = Column(Integer, ForeignKey(Target.id))

    target = relationship("Target", back_populates="notes")


class Mission(BaseModel):
    is_completed = Column(Boolean, default=False, nullable=True)

    # Keys
    assigned_to = Column(Integer, ForeignKey(SpyCat.id), nullable=True)
    target_id = Column(Integer, ForeignKey(Target.id))

    # Relations
    target = relationship("Target", back_populates="missions")
    spy_cat = relationship("SpyCat", back_populates="missions")
