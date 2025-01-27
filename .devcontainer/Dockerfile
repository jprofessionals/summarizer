FROM python:3.12.7-slim

RUN pip install uv
# RUN uv venv --python 3.12.7

WORKDIR /app
RUN --mount=source=dist,target=/dist uv pip install --no-cache /dist/*.whl
CMD python -m summarizer
