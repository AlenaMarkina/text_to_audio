from fastapi import APIRouter

from api.v1.routes.city import router as city_router
from api.v1.routes.place_of_interest import router as place_router
from api.v1.routes.image import router as image_route
from api.v1.routes.description import router as description_router
from api.v1.routes.audio import router as audio_router

router = APIRouter(prefix="/api/text_to_audio/v1")

router.include_router(city_router, prefix="/cites", tags=["Города"])
router.include_router(place_router, prefix="/places", tags=["Достопримечательности"])
router.include_router(image_route, prefix="/images", tags=["Фотографии"])
router.include_router(description_router, prefix="/description", tags=["Описание достопримечательностей"])
router.include_router(audio_router, prefix="/audio", tags=["Аудиозаписи к достопримечательностям"])
