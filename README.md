# Summarizer

Summarizers for:
1. Summarizing job listings
2. Summarizing experience extracted from CVs to fill "komeptanse matriser"
3. Summarizing CVs down to X number of pages - and also specializing into spesific fields.


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


### Build infra structure
```
terraform init --upgrade
terraform plan -out=tfplan
terraform apply tfplan
//  terraform destroy
```

### Build initial docker image and send it to the Container registry
```
<!-- ACR_LOGIN_SERVER=$(terraform output -raw acr_login_server) -->
ACR_LOGIN_SERVER=$(terraform -chdir=terraform output -raw acr_login_server)
<!-- echo $ACR_LOGIN_SERVER -->
docker build -t ${ACR_LOGIN_SERVER}/summarizer-app:latest .
<!-- az acr login --name $(echo ${ACR_LOGIN_SERVER} | cut -d'.' -f1) -->
az acr login --name $(echo ${ACR_LOGIN_SERVER})
docker push ${ACR_LOGIN_SERVER}/summarizer-app:latest
```
