# Summarizer

Summarizers for:
1. Summarizing job listings
2. Summarizing experience extracted from CVs to fill "komeptanse matriser"


## Setup
- Build the project python virtualenvironment
    - ``uv sync``
        - This should setup your virtual environment (based on pyproject.toml) and fix any ipykernel issues.
- Setup the precommits setup for the project
    - ``pre-commit install``
- Verify you can build the Dockerfile
    - ``docker build .``
    - ``docker build -t summarizer:latest .``
    - To run this locally for testing
        - ``docker run -d -p 80:80 summarizer-app``
- To run streamlit apps
    - ``streamlit run src/summarizer/apps/streamlit_app.py``
    - ``streamlit run src/summarizer/apps/streamlit_matrices_app.py``
- To run fastapi apps
    - ``uvicorn src.summarizer.apps.fastapi_app:app --reload``
