from fastapi import APIRouter

from api.v1.routes.city import router as city_router

router = APIRouter(prefix="/api/text_to_audio/v1")

router.include_router(city_router, prefix="/cites", tags=["Города"])
