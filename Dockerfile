# 1. 경량 Python 베이스 이미지 사용
FROM python:3.9-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 앱 코드 복사
COPY app.py .

# 5. 컨테이너 시작 시 실행할 명령
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]