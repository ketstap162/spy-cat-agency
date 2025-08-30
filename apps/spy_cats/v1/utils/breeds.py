import httpx
from fastapi import HTTPException
from datetime import datetime, timedelta

from api.core.settings import settings
from db.utils.dt import get_now


class BreedsCache:
    breeds: list[str] | None = None
    last_update: datetime | None = None


async def get_cat_breeds():
    if (
        BreedsCache.breeds is not None
        and BreedsCache.last_update is not None
        and get_now() - BreedsCache.last_update < timedelta(minutes=15)
    ):
        return BreedsCache.breeds

    async with httpx.AsyncClient() as client:
        response = await client.get(settings.CAT_API_URL)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch breeds from TheCatAPI"
        )

    data = response.json()
    breeds = [breed["name"] for breed in data]

    BreedsCache.breeds = breeds
    BreedsCache.last_update = datetime.utcnow()

    return breeds
