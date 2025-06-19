# C:\Users\jun\anaconda3\python.exe -m uvicorn app.app:app --reload 
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import slope ,hospital  

app = FastAPI(title="Slope DEM API")

# --- CORS 설정 ---
origins = [
    "http://localhost:3000",     # React 개발용 (포트 3000)
    "http://127.0.0.1:3000",
    # 배포 시 도메인 추가
    # "https://your-production-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # 허용할 origin
    allow_credentials=True,
    allow_methods=["*"],             # 모든 메서드 허용 (GET, POST 등)
    allow_headers=["*"],             # 모든 헤더 허용
)

# --- 라우터 등록 ---
app.include_router(slope.router, prefix="/api/slope", tags=["Slope Analysis"])
app.include_router(hospital.router, prefix="/api/hospital", tags=["Hospital"])

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)