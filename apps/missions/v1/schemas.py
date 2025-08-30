from typing import Optional

from pydantic import BaseModel

from apps.spy_cats.v1.schemas import SpyCatInfo


class ConfiguredModel(BaseModel):
    class Config:
        from_attributes = True


class MissionListed(ConfiguredModel):
    id: Optional[int]
    target_id: Optional[int]
    assigned_to: Optional[int]
    is_completed: Optional[bool]


class TargetForm(BaseModel):
    name: str
    country: str
    notes: list[str]


class TargetNoteDetail(ConfiguredModel):
    id: Optional[int]
    note: Optional[str]
    target_id: Optional[int]


class TargetDetail(ConfiguredModel):
    name: Optional[str]
    country: Optional[str]
    notes: Optional[list[TargetNoteDetail]]


class MissionForm(BaseModel):
    target: TargetForm
    assigned_to: int
    is_completed: Optional[bool] = False


class MissionDetail(ConfiguredModel):
    id: Optional[int]
    is_completed: Optional[bool]
    target: Optional[TargetDetail]
    spy_cat: Optional[SpyCatInfo]


class MissionUpdateForm(BaseModel):
    is_completed: Optional[bool] = None
    target_notes: Optional[list[str]] = None
    replace_target_notes: bool = False
    assign_to: Optional[int] = None
    unassign: bool = False
