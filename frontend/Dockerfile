# 1. nginx 베이스 이미지 사용
FROM nginx:stable-alpine

# 2. 기본 nginx 설정 삭제 (선택)
RUN rm -rf /usr/share/nginx/html/*

# 3. React 빌드 결과 복사
COPY build /usr/share/nginx/html

# 4. 80포트 오픈 (nginx 기본)...
EXPOSE 80

# 5. nginx 실행 (기본 CMD 사용)