import streamlit as st
import json
from summarizer import document_utils
from summarizer.summarizers import matrices

def parse_requirements_text(requirements_text: str) -> dict:
    """
    Parses the requirements text into a dictionary, skipping lines that cannot be converted.

    Args:
        requirements_text (str): The requirements text.

    Returns:
        dict: The parsed requirements dictionary.
    """
    requirements = {}
    for line in requirements_text.splitlines():
        try:
            key, value = line.split(":", 1)
            requirements[key.strip()] = value.strip()
        except ValueError:
            # Skip lines that cannot be split into key-value pairs
            continue
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

                # Extract text from requirements DOCX
                requirements_text = document_utils.extract_text_from_docx(requirements_file)

                # Convert requirements text to dictionary
                requirements = parse_requirements_text(requirements_text)

                with st.spinner("Filling requirements matrix..."):
                    filled_matrix = matrices.fill_requirements_matrix_with_openai(
                        cv=cv_text,
                        requirements=requirements,
                        system_prompt=system_prompt,
                        user_prompt=user_prompt
                    )
                st.subheader("Filled Requirements Matrix:")
                st.text_area("Suggested text", value=filled_matrix, height=300)
                # st.json(filled_matrix)
            except Exception as e:
                st.error(f"Error filling requirements matrix: {e}")
        else:
            st.error("Please upload both the CV and the requirements matrix files.")

if __name__ == "__main__":
    main()

# To run the Streamlit app, use the following command:
# streamlit run src/summarizer/apps/streamlit_matrices_app.py