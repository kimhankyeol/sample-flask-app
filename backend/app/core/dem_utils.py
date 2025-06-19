# dem_utils.py
import numpy as np
import rasterio
from pyproj import Transformer
from .slope_config import COLORS, DIRECTION_MAP

class DEMProcessor:
    def __init__(self, dem_path):
        self.ds = rasterio.open(dem_path)
        self.dem = self.ds.read(1).astype(float)
        self.transform = self.ds.transform
        self.crs = self.ds.crs
        self.width = self.ds.width
        self.height = self.ds.height
        self.nodata = self.ds.nodata
        if self.nodata is not None:
            self.dem[self.dem == self.nodata] = np.nan

        self.to_latlon = Transformer.from_crs(self.crs, "EPSG:4326", always_xy=True)
        self.to_pixel = Transformer.from_crs("EPSG:4326", self.crs, always_xy=True)

    def latlon_to_pixel(self, lat, lon):
        x, y = self.to_pixel.transform(lon, lat)
        col, row = ~self.transform * (x, y)
        return int(row), int(col)

    def pixel_to_latlon(self, row, col):
        x, y = rasterio.transform.xy(self.transform, row, col, offset='center')
        lon, lat = self.to_latlon.transform(x, y)
        return lat, lon

    def get_color(self, slope):
        for low, high, color in COLORS:
            if low <= slope <= high:
                return color
        return None

    def get_direction(self, dr, dc):
        return DIRECTION_MAP.get((dr, dc), "↑")

    def compute_distance(self, r1, c1, r2, c2):
        lat1, lon1 = self.pixel_to_latlon(r1, c1)
        lat2, lon2 = self.pixel_to_latlon(r2, c2)
        dx = (lon2 - lon1) * 111320 * np.cos(np.radians((lat1 + lat2) / 2))
        dy = (lat2 - lat1) * 110540
        return np.sqrt(dx**2 + dy**2)
    def analyze(self, center_lat, center_lon, radius_m=1000, grid_max=50):  # grid_max 기본값을 50으로 변경
        center_row, center_col = self.latlon_to_pixel(center_lat, center_lon)
        pixel_size_x = abs(self.transform.a)
        pixel_size_y = abs(self.transform.e)

        radius_px_x = int(radius_m / pixel_size_x)
        radius_px_y = int(radius_m / pixel_size_y)

        row_start = max(center_row - radius_px_y, 0)
        row_end = min(center_row + radius_px_y, self.height)
        col_start = max(center_col - radius_px_x, 0)
        col_end = min(center_col + radius_px_x, self.width)

        step_row = max(1, (row_end - row_start) // grid_max)
        step_col = max(1, (col_end - col_start) // grid_max)

        grid_data = []

        for row in range(row_start, row_end - step_row, step_row):
            for col in range(col_start, col_end - step_col, step_col):
                center_r = row + step_row // 2
                center_c = col + step_col // 2

                if np.isnan(self.dem[center_r, center_c]):
                    continue

                max_slope, best_arrow = 0, None

                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = center_r + dr, center_c + dc
                        if nr < 0 or nr >= self.height or nc < 0 or nc >= self.width:
                            continue
                        if np.isnan(self.dem[nr, nc]):
                            continue

                        dh = self.dem[nr, nc] - self.dem[center_r, center_c]
                        dist = self.compute_distance(center_r, center_c, nr, nc)
                        if dist == 0:
                            continue
                        slope = abs(dh) / dist * 100
                        if slope > max_slope:
                            max_slope = slope
                            best_arrow = self.get_direction(dr, dc)

                color = self.get_color(max_slope)
                if color:
                    lat_c, lon_c = self.pixel_to_latlon(center_r, center_c)
                    grid_data.append({
                        "lat": lat_c,
                        "lon": lon_c,
                        "slope": round(max_slope, 2),
                        "arrow": best_arrow,
                        "color": color
                    })

        return grid_data
    # grid_max=100   50~70
    # def analyze(self, center_lat, center_lon, radius_m=1000, grid_max=50): 
        center_row, center_col = self.latlon_to_pixel(center_lat, center_lon)
        pixel_size_x = abs(self.transform.a)
        pixel_size_y = abs(self.transform.e)

        radius_px_x = int(radius_m / pixel_size_x)
        radius_px_y = int(radius_m / pixel_size_y)

        row_start = max(center_row - radius_px_y, 0)
        row_end = min(center_row + radius_px_y, self.height)
        col_start = max(center_col - radius_px_x, 0)
        col_end = min(center_col + radius_px_x, self.width)

        step_row = max(1, (row_end - row_start) // grid_max)
        step_col = max(1, (col_end - col_start) // grid_max)

        grid_data = []

        for row in range(row_start, row_end - step_row, step_row):
            for col in range(col_start, col_end - step_col, step_col):
                center_r = row + step_row // 2
                center_c = col + step_col // 2

                if np.isnan(self.dem[center_r, center_c]):
                    continue

                max_slope, best_arrow = 0, None

                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = center_r + dr, center_c + dc
                        if nr < 0 or nr >= self.height or nc < 0 or nc >= self.width:
                            continue
                        if np.isnan(self.dem[nr, nc]):
                            continue

                        dh = self.dem[nr, nc] - self.dem[center_r, center_c]
                        dist = self.compute_distance(center_r, center_c, nr, nc)
                        if dist == 0:
                            continue
                        slope = abs(dh) / dist * 100
                        if slope > max_slope:
                            max_slope = slope
                            best_arrow = self.get_direction(dr, dc)

                color = self.get_color(max_slope)
                if color:
                    lat_c, lon_c = self.pixel_to_latlon(center_r, center_c)
                    grid_data.append({
                        "lat": lat_c,
                        "lon": lon_c,
                        "slope": round(max_slope, 2),
                        "arrow": best_arrow,
                        "color": color
                    })

        return grid_data