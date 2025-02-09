# Dockerfile

# 1. Python 3.9-slim 이미지를 베이스 이미지로 사용
FROM python:3.9-slim

# 2. Python이 .pyc 파일을 생성하지 않도록 하고, 표준 출력을 버퍼링하지 않도록 환경변수 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 의존성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. 애플리케이션 소스 코드 복사
COPY . /app/

# 6. 컨테이너 실행 시 Gunicorn으로 애플리케이션 구동 (포트 8000 사용)
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:${PORT:-8000}"]
