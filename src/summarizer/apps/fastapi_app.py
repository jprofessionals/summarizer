from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from typing import List
from summarizer import document_utils
from summarizer.summarizers import joblistings, matrices, cv_adjuster

app = FastAPI()


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


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    """
    Serve the favicon.
    """
    return FileResponse("static/favicon.ico")


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
            elif (
                uploaded_file.content_type
                == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ):
                text = document_utils.extract_text_from_docx(uploaded_file.file)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {uploaded_file.content_type}",
                )

            all_text += text + "\n"
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error extracting text from file {uploaded_file.filename}: {e}",
            )

    if not all_text:
        raise HTTPException(
            status_code=400, detail="No text extracted from the documents."
        )

    return all_text


@app.post("/summarize/")
async def summarize_files(
    files: List[UploadFile] = File(...),
    system_prompt: str = joblistings.dict_roles["system"],
    user_prompt: str = joblistings.dict_roles["user"],
) -> JSONResponse:
    """
    Endpoint to summarize the text extracted from the uploaded files.

    Args:
        files (List[UploadFile]): The uploaded files.
        system_prompt (str): The system prompt for the OpenAI API.
        user_prompt (str): The user prompt for the OpenAI API.

    Returns:
        JSONResponse: The summary of the text.
    """
    all_text = handle_text_extraction_from_files(files)

    try:
        summary = joblistings.summarize_text_with_openai(
            all_text, system_prompt, user_prompt
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {e}")

    return JSONResponse(content={"summary": summary})


# class FillRequirementsResponse(BaseModel):
#     filled_requirements: dict


@app.post("/fill_requirements/")
async def fill_requirements(
    cv_file: UploadFile = File(...),
    requirements_file: UploadFile = File(...),
    system_prompt: str = matrices.dict_roles["system"],
    user_prompt: str = matrices.dict_roles["user"],
) -> JSONResponse:
    """
    Endpoint to fill out requirements based on a consultant's CV.

    Args:
        cv_file (UploadFile): The uploaded CV file (PDF).
        requirements_file (UploadFile): The uploaded requirements file (DOCX).

    Returns:
        FillRequirementsResponse: The filled requirements.
    """
    try:
        if cv_file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="CV file must be a PDF.")
        if (
            requirements_file.content_type
            != "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            raise HTTPException(
                status_code=400, detail="Requirements file must be a DOCX."
            )

        cv_text = document_utils.extract_text_from_pdf(cv_file.file)
        # requirements_text = document_utils.extract_text_from_docx(requirements_file.file)

        # Extract matrix-like data from requirements DOCX
        requirements_dict = document_utils.extract_requirements_from_docx(
            requirements_file.file
        )

        # Format extracted requirements for display
        requirements_text = document_utils.format_requirements_for_display(
            requirements_dict
        )

        print(requirements_text)

        # # Combine all requirements into one prompt
        #     combined_requirements = f"{user_prompt}\n\n{confirmed_requirements}"

        filled_response = matrices.fill_requirement_with_openai(
            cv=cv_text,
            requirement=requirements_text,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        # requirements_list = requirements_text.split("\n")  # Assuming each requirement is on a new line

        # filled_requirements = {}
        # for requirement in requirements_list:
        #     filled_requirements[requirement] = matrices.fill_requirement_with_openai(
        #         cv=cv_text,
        #         requirement=requirement,
        #         system_prompt=matrices.dict_roles["system"],
        #         user_prompt=matrices.dict_roles["user"],
        #     )
        # return FillRequirementsResponse(filled_requirements=filled_requirements)
        return JSONResponse(content={"filled_response": filled_response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error filling requirements: {e}")


@app.post("/shorten_cv/")
async def shorten_cv(
    files: List[UploadFile] = File(...), pages: int = 1
) -> JSONResponse:
    """
    Endpoint to shorten the CV to fit a specified number of pages.

    Args:
        files (List[UploadFile]): The uploaded files.
        pages (int): The number of pages the CV should be shortened to.

    Returns:
        JSONResponse: The shortened CV.
    """
    all_text = handle_text_extraction_from_files(files)

    try:
        shortened_cv = cv_adjuster.shorten_cv_with_openai(cv=all_text, pages=pages)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating shortened CV: {e}"
        )

    return JSONResponse(content={"shortened_cv": shortened_cv})


# To run the FastAPI app, use the following command:
# uvicorn src.summarizer.apps.fastapi_app:app --reload
