from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from summarizer import document_utils, openai_summarizer

app = FastAPI()

class SummarizeRequest(BaseModel):
    system_prompt: str = openai_summarizer.dict_roles["system"]
    user_prompt: str = openai_summarizer.dict_roles["user"]

class SummarizeResponse(BaseModel):
    summary: str

@app.get("/")
def read_root() -> dict:
    """
    Root endpoint to verify that the API is running.
    """
    return {"Response": "Hello from the Summarizer API!"}

@app.get("/health")
async def health_check() -> JSONResponse:
    """
    Health check endpoint to verify that the API is running.
    """
    return JSONResponse(content={"status": "ok"})

def handle_text_extraction_from_files(files: List[UploadFile]) -> str:
    """
    Extracts text from the uploaded files.

    Args:
        files (List[UploadFile]): The uploaded files.

    Returns:
        str: The extracted text from the files.
    """
    all_text = ""
    for uploaded_file in files:
        try:
            if uploaded_file.content_type == "application/pdf":
                text = document_utils.extract_text_from_pdf(uploaded_file.file)
            elif uploaded_file.content_type == "text/plain":
                text = document_utils.extract_text_from_txt(uploaded_file.file)
            elif uploaded_file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = document_utils.extract_text_from_docx(uploaded_file.file)
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {uploaded_file.content_type}")

            all_text += text + "\n"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error extracting text from file {uploaded_file.filename}: {e}")

    if not all_text:
        raise HTTPException(status_code=400, detail="No text extracted from the documents.")
    
    return all_text

@app.post("/summarize/", response_model=SummarizeResponse)
async def summarize_files(
    files: List[UploadFile] = File(...),
    request: SummarizeRequest = SummarizeRequest()
) -> SummarizeResponse:
    """
    Endpoint to summarize the text extracted from the uploaded files.

    Args:
        files (List[UploadFile]): The uploaded files.
        request (SummarizeRequest): The request containing system and user prompts.

    Returns:
        SummarizeResponse: The summary of the text.
    """
    all_text = handle_text_extraction_from_files(files)

    try:
        summary = openai_summarizer.summarize_text_with_openai(all_text, request.system_prompt, request.user_prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {e}")

    return SummarizeResponse(summary=summary)

# To run the FastAPI app, use the following command:
# uvicorn src.summarizer.apps.fastapi_app:app --reload