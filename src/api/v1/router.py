from fastapi import APIRouter

from api.v1.routes.city import router as city_router
from api.v1.routes.landmark import router as landmark_router
from api.v1.routes.image import router as image_route
from api.v1.routes.description import router as description_router
from api.v1.routes.audio import router as audio_router
from api.v1.routes.country import router as country_router

router = APIRouter(prefix="/api/text_to_audio/v1")

router.include_router(city_router, prefix="/cites", tags=["Города"])
router.include_router(country_router, prefix="/countries", tags=["Страны"])
router.include_router(landmark_router, prefix="/landmarks", tags=["Достопримечательности"])
router.include_router(image_route, prefix="/images", tags=["Фотографии"])
router.include_router(description_router, prefix="/description", tags=["Описание достопримечательностей"])
router.include_router(audio_router, prefix="/audio", tags=["Аудиозаписи к достопримечательностям"])
