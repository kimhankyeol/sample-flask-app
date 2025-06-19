# 1. Python 베이스 이미지 선택 (가볍고 안정적인 버전)
FROM python:3.9-slim

# 2. 작업 디렉터리 설정
WORKDIR /app

# 3. 필요한 파일 복사 (requirements.txt 파일을 backend/에 위치했다고 가정)
COPY requirements.txt .

# 4. 의존성 설치 (uvicorn, fastapi 등)
RUN pip install --no-cache-dir -r requirements.txt

# 5. 앱 소스 전체 복사
COPY app ./app

# 6. 컨테이너 시작 시 uvicorn으로 FastAPI 앱 실행
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]