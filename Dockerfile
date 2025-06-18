# 1. 경량 Python 베이스 이미지 사용
FROM python:3.9-slim

# 2. 컨테이너 내부 작업 디렉토리 설정
WORKDIR /app

# 3. 필요한 파일 복사
COPY requirements.txt .

# 4. 라이브러리 설치 (캐시 사용 안 함 → 이미지 경량화)
RUN pip install --no-cache-dir -r requirements.txt

# 5. 앱 코드 복사
COPY app.py .

# 6. 컨테이너 시작 시 실행할 명령
CMD ["python", "app.py"]