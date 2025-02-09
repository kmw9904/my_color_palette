# Dockerfile

# 1. Python 3.9-slim 이미지를 베이스 이미지로 사용
FROM python:3.9-slim

# 2. 필요한 시스템 패키지 업데이트 및 설치 (libGL 및 libglib 관련 패키지 추가)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Python 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. 작업 디렉토리 설정
WORKDIR /app

# 5. 의존성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. 애플리케이션 소스 코드 복사
COPY . /app/

# 7. 컨테이너 실행 시 Gunicorn으로 애플리케이션 구동 (환경 변수 PORT 사용)
CMD sh -c "gunicorn backend.wsgi:application --bind 0.0.0.0:${PORT:-8000}"
