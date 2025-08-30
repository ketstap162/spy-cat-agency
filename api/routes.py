from fastapi import APIRouter
from apps.spy_cats.v1.controllers import router as spy_cat_router_v1
from apps.missions.v1.controllers import router as mission_router_v1

main_router = APIRouter()

main_router.include_router(spy_cat_router_v1, prefix="/spi_cats", tags=["spi_cats"])
main_router.include_router(mission_router_v1, prefix="/missions", tags=["missions"])
