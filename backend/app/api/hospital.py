# app/api/hospital.py

from fastapi import APIRouter, HTTPException
import pandas as pd

router = APIRouter()

# 병원 데이터 로딩
HOSPITAL_PATH = "./app/data/hospital_data.csv"

@router.get("/markers")
def get_hospitals():
   
    try:
        df = pd.read_csv(HOSPITAL_PATH)
        df.rename(columns={'병원/약국명':'name', 'latitude':'lat', 'longitude':'lon','시군구명':'district'}, inplace = True)
        # hospitals = [
        #     {
        #         "name": row["병원/약국명"],
        #         "lat": row["latitude"],
        #         "lon": row["longitude"]
        #     }
        #     for _, row in df.iterrows()
        # ]
        return df[["lat","lon","name","district"]].to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
