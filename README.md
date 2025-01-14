# Summarizer

Describe your project here.


## Setup
- Build the project python virtualenvironment
    - ``rye sync``
        - This should setup your virtual environment (based on pyproject.toml) and fix any ipykernel issues.
- Setup the precommits setup for the project
    - ``pre-commit install``
- Verify you can build the Dockerfile
    - ``docker build .``
    - ``docker build -t summarizer:latest .``