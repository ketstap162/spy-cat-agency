from fastapi import APIRouter, HTTPException
from sqlalchemy import delete
from sqlalchemy.orm import joinedload
from starlette import status

from api.core.dependencies import Deps
from db.models.missions import Mission, Target, TargetNote
from db.models import missions as app_models
from db.models.spy_cats import SpyCat
from db.session import Session
from . import schemas

router = APIRouter()


@router.get("/")
async def get_mission_list(
        session: Session = Deps.get_session()
) -> list[schemas.MissionListed]:
    query = Mission.get()

    async with session.async_() as db:
        result = await db.execute(query)
        missions = result.scalars().all()

        return [
            schemas.MissionListed.from_orm(mission)
            for mission in missions
        ]


@router.post("/")
async def create_mission(
        form: schemas.MissionForm,
        session: Session = Deps.get_session()
):
    async with session.async_() as db:
        if form.assigned_to:
            query = SpyCat.get(id=form.assigned_to)
            result = await db.execute(query)
            cat = result.scalars().one_or_none()

            if not cat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Cat with id={form.assigned_to} not found."
                )

        target = app_models.Target(
            name=form.target.name,
            country=form.target.country
        )

        db.add(target)
        await db.flush()

        notes = [
            app_models.TargetNote(
                target_id=target.id,
                note=note
            )
            for note in form.target.notes
        ]

        db.add_all(notes)

        mission = Mission(
            target_id=target.id,
            assigned_to=form.assigned_to
        )

        if form.is_completed:
            mission.is_completed = form.is_completed

        db.add(mission)
        await db.commit()

    return "Mission created"


@router.get("/{mission_id}")
async def get_mission_detail(
        mission_id: int,
        session: Session = Deps.get_session()
) -> schemas.MissionDetail:
    query = Mission.get(id=mission_id).options(
        joinedload(Mission.target).joinedload(Target.notes),
        joinedload(Mission.spy_cat),
    )

    async with session.async_() as db:
        result = await db.execute(query)
        mission = result.unique().scalars().one_or_none()

        return schemas.MissionDetail.from_orm(mission)


@router.patch("/{mission_id}")
async def update_mission(
        mission_id: int,
        form: schemas.MissionUpdateForm,
        session: Session = Deps.get_session()
):
    query = Mission.get(id=mission_id).options(
        joinedload(Mission.target).joinedload(Target.notes),
    )

    async with session.async_() as db:
        result = await db.execute(query)
        mission = result.unique().scalars().one_or_none()

        if not mission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mission with id={mission_id} not found."
            )

        if form.is_completed is not None:
            mission.is_completed = form.is_completed

        if form.target_notes:
            if form.replace_target_notes:
                query = (
                    delete(TargetNote)
                    .where(
                        TargetNote.id.in_([note.id for note in mission.target.notes])
                    )
                )

                await db.execute(query)

            notes = [
                TargetNote(
                    target_id=mission.target.id,
                    note=note
                )
                for note in form.target_notes
            ]

            db.add_all(notes)

        if form.unassign:
            mission.assigned_to = None

        elif form.assign_to:
            query = SpyCat.get(id=form.assign_to)
            result = await db.execute(query)
            cat = result.scalars().one_or_none()

            if not cat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Cat with id={form.assign_to} not found."
                )

            mission.assigned_to = form.assign_to

        await db.commit()

    return f"Mission with id={mission_id} updated successfully."
