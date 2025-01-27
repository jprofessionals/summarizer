from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from summarizer import document_utils, openai_utils

app = FastAPI()

@app.post("/summarize/")
async def summarize_files(
    files: List[UploadFile] = File(...),
    system_prompt: str = openai_utils.dict_roles["system"], # We don't expect the user to provide the system prompt
    user_prompt: str = openai_utils.dict_roles["user"] # We don't expect the user to provide the user prompt
):
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

    try:
        summary = openai_utils.summarize_text_with_openai(all_text, system_prompt, user_prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {e}")

    return JSONResponse(content={"summary": summary})

# To run the FastAPI app, use the following command:
# uvicorn src.summarizer.apps.fastapi_app:app --reload