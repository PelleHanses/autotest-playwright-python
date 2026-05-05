# Python-basimage
#FROM python:3.12-slim
FROM docker.io/library/playwright_python:fk
 
# Undvik interaktiva apt-frågor
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
 
# Installera systemberoenden som Playwright behöver
 
# Uppgradera pip
 
# Installera Python Playwright + deps
 
# Installera browsers (Chromium räcker oftast)
 
# Arbetskatalog
WORKDIR /work
 
# Kopiera tester
COPY ./app/ /work

ENTRYPOINT ["python", "runner.py"]
#CMD ["--help"]
 
# Standardkommando (kan overridas)
#CMD ["python", "runner.py", "--help"]

