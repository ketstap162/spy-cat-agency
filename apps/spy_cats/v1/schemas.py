from typing import Optional

from pydantic import BaseModel


class ConfiguredModel(BaseModel):
    class Config:
        from_attributes = True


class SpyCatInfo(ConfiguredModel):
    id: Optional[int]
    name: Optional[str]
    exp_years: Optional[int]
    breed: Optional[str]
    salary: Optional[float]


class SpyCatForm(BaseModel):
    name: str
    exp_years: int
    breed: str
    salary: float


class SpyCatCreationConfirm(BaseModel):
    message: Optional[str]
    cat_info: SpyCatInfo


class SpyCatUpdateForm(BaseModel):
    salary: Optional[float]


class SpyCatUpdateConfirmation(BaseModel):
    message: Optional[str]
    cat_info: SpyCatInfo
