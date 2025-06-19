from app.models.slope_model import SlopeRequest, SlopeResponse, SlopeCell
from app.utils.dem_utils import load_dem, analyze_dem_area

def analyze_slope(data: SlopeRequest) -> SlopeResponse:
    dem, transform, crs = load_dem("your_dem_file.img")
    cells = analyze_dem_area(dem, transform, crs, data)
    return SlopeResponse(
        center_lat=data.center_lat,
        center_lon=data.center_lon,
        cells=cells
    )