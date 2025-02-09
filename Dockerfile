# Dockerfile

FROM python:3.9

# 필요한 시스템 패키지 업데이트 및 설치 (OpenCV 및 cv2가 의존하는 라이브러리 포함)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgthread-2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

CMD sh -c "gunicorn backend.wsgi:application --bind 0.0.0.0:${PORT:-8000}"
