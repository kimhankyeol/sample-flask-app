from fastapi import APIRouter, Query
from app.core.dem_utils import DEMProcessor
import os

router = APIRouter()

DEM_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "your_dem_file.img")
dem_processor = DEMProcessor(DEM_PATH)

@router.get("/grid")
def get_slope_data(
    lat: float = Query(..., description="중심 위도"),
    lon: float = Query(..., description="중심 경도"),
    radius: int = Query(1000, description="반경 (미터)"),
    grid: int = Query(100, description="최대 격자 수")
):
    result = dem_processor.analyze(lat, lon, radius, grid)
    return  result