from fastapi import APIRouter, HTTPException
from starlette import status

from api.core.dependencies import Deps
from db.models.spy_cats import SpyCat
from db.session import Session
from . import schemas
from .utils.breeds import get_cat_breeds

router = APIRouter()


@router.get("/")
async def get_cat_list(
        session: Session = Deps.get_session()
) -> list[schemas.SpyCatInfo]:
    query = SpyCat.get()

    async with session.async_() as db:
        result = await db.execute(query)
        cats = result.scalars().all()

    return [
        schemas.SpyCatInfo.from_orm(cat)
        for cat in cats
    ]


@router.post("/")
async def create_cat(
        form: schemas.SpyCatForm,
        session: Session = Deps.get_session()
):
    breeds = await get_cat_breeds()

    if form.breed not in breeds:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported breed. You can use following breeds: {breeds}"
        )

    new_cat = SpyCat(**form.dict())

    async with session.async_() as db:
        db.add(new_cat)
        await db.commit()
        await db.refresh(new_cat)

        return schemas.SpyCatCreationConfirm(
            message="Spy Cat created successfully.",
            cat_info=new_cat,
        )


@router.get("/{cat_id}")
async def get_cat_detail(
        cat_id: int,
        session: Session = Deps.get_session()
):
    query = SpyCat.get(id=cat_id)

    async with session.async_() as db:
        result = await db.execute(query)
        cat = result.scalars().one_or_none()

        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cat with id={cat_id} not found."
            )
        return schemas.SpyCatInfo.from_orm(cat)


@router.patch("/{cat_id}")
async def update_cat(
        cat_id: int,
        form: schemas.SpyCatUpdateForm,
        session: Session = Deps.get_session()
):
    form_dict = form.dict(exclude_unset=True)

    if not form_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nothing to update."
        )

    query = SpyCat.get(id=cat_id)

    async with session.async_() as db:
        result = await db.execute(query)
        cat = result.scalars().one_or_none()

        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cat with id={cat_id} not found."
            )

        for field, value in form_dict.items():
            setattr(cat, field, value)

        await db.commit()
        await db.refresh(cat)

        return schemas.SpyCatUpdateConfirmation(
            message=f"Cat with id={cat_id} updated successfully.",
            cat_info=cat,
        )


@router.delete("/{cat_id}")
async def delete_cat(
        cat_id: int,
        session: Session = Deps.get_session()
):
    query = SpyCat.get(id=cat_id)

    async with session.async_() as db:
        result = await db.execute(query)
        cat = result.scalars().one_or_none()

        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cat with id={cat_id} not found."
            )

        await db.delete(cat)
        await db.commit()

    return f"Cat with id={cat_id} deleted successfully."
