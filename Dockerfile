FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


ENV TRANSFORMERS_CACHE=app/model/model_cache

RUN python -m unittest discover tests

EXPOSE 8000

RUN useradd -m myuser
USER myuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]