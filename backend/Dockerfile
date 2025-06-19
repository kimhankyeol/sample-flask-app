# 1. Python 베이스 이미지 선택 (가볍고 안정적인 버전)..
FROM python:3.9-slim

# 시스템 빌드 툴 및 라이브러리 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# GDAL 관련 환경변수 세팅 (rasterio 설치 위해)
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]