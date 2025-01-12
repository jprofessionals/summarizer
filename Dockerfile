FROM python:3.12.7-slim

RUN pip install uv
# RUN uv venv --python 3.12.7

WORKDIR /app
COPY requirements.lock ./
RUN uv pip install --no-cache --system -r requirements.lock

COPY src .
CMD ["python", "main.py"]
