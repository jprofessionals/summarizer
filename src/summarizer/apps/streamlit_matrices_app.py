import streamlit as st
from summarizer import document_utils
from summarizer.summarizers import matrices
import docx

def extract_requirements_from_docx(docx_file) -> dict:
    """
    Extracts matrix-like data from the requirements DOCX file.

    Args:
        docx_file (file-like object): The DOCX file to extract requirements from.

    Returns:
        dict: A dictionary of requirements extracted from the DOCX file.
    """
    requirements = {}
    doc = docx.Document(docx_file)
    for table in doc.tables:
        headers = [cell.text.strip() for cell in table.rows[0].cells]
        for row in table.rows[1:]:
            cells = row.cells
            for i, header in enumerate(headers):
                key = header
                value = cells[i].text.strip()
                if key and value:
                    if key not in requirements:
                        requirements[key] = []
                    requirements[key].append(value)
    return requirements

def main() -> None:
    """
    Main function of the Streamlit app for filling out requirements matrices.
    """
    st.set_page_config(
        page_title="Requirements Matrix Filler", 
        # layout="wide"
    )

    st.title("Requirements Matrix Filler")

    # Text input for system and user prompts
    system_prompt = st.text_area(
        "System Prompt",
        value=matrices.dict_roles["system"],
        height=150
    )

    user_prompt = st.text_area(
        "User Prompt",
        value=matrices.dict_roles["user"],
        height=150
    )

    # File upload for CV (PDF)
    cv_file = st.file_uploader(
        "Upload Consultant's CV (PDF)",
        type=["pdf"]
    )

    # File upload for requirements matrix (DOCX)
    requirements_file = st.file_uploader(
        "Upload Requirements Matrix (DOCX)",
        type=["docx"]
    )

    if st.button("Fill Requirements Matrix"):
        if cv_file and requirements_file:
            try:
                # Extract text from CV PDF
                cv_text = document_utils.extract_text_from_pdf(cv_file)

                # Extract matrix-like data from requirements DOCX
                requirements_dict = extract_requirements_from_docx(requirements_file)

                # Display extracted requirements for user confirmation or modification
                st.subheader("Extracted Requirements:")
                requirements_input = st.text_area(
                    "Please confirm or modify the extracted requirements:",
                    value="\n".join([f"{key}: {', '.join(values)}" for key, values in requirements_dict.items()]),
                    height=300
                )

                if st.button("Confirm and Fill Requirements Matrix"):
                    # Convert confirmed/modified requirements to a list
                    confirmed_requirements = requirements_input.splitlines()

                    filled_matrix = {}
                    with st.spinner("Filling requirements matrix..."):
                        for requirement in confirmed_requirements:
                            if requirement.strip():
                                filled_response = matrices.fill_requirement_with_openai(
                                    cv=cv_text,
                                    requirement=requirement,
                                    system_prompt=system_prompt,
                                    user_prompt=user_prompt
                                )
                                filled_matrix[requirement] = filled_response

                    st.subheader("Filled Requirements Matrix:")
                    st.json(filled_matrix)
            except Exception as e:
                st.error(f"Error filling requirements matrix: {e}")
        else:
            st.error("Please upload both the CV and the requirements matrix files.")

if __name__ == "__main__":
    main()

# To run the Streamlit app, use the following command:
# streamlit run src/summarizer/apps/streamlit_matrices_app.py