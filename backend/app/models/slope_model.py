from pydantic import BaseModel
from typing import List

class SlopeCell(BaseModel):
    lat: float
    lon: float
    slope: float
    direction: str
    color: str

class SlopeRequest(BaseModel):
    center_lat: float
    center_lon: float
    radius: int = 1000  # m
    grid_size: int = 30

class SlopeResponse(BaseModel):
    center_lat: float
    center_lon: float
    cells: List[SlopeCell]