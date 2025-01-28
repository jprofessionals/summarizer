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

def format_requirements_for_display(requirements_dict: dict) -> str:
    """
    Formats the requirements dictionary for display, adding numbering for each line.

    Args:
        requirements_dict (dict): The dictionary of requirements.

    Returns:
        str: The formatted string of requirements.
    """
    formatted_requirements = []
    counter = 1
    for key, values in requirements_dict.items():
        for value in values:
            formatted_requirements.append(f"{counter}. {key}: {value}")
            counter += 1
    return "\n".join(formatted_requirements)

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

    formatted_requirements = ""
    if st.button("Extract Requirements"):
        if cv_file and requirements_file:
            try:


                # Extract matrix-like data from requirements DOCX
                requirements_dict = extract_requirements_from_docx(requirements_file)

                # Format extracted requirements for display
                formatted_requirements = format_requirements_for_display(requirements_dict)

                # Store the extracted requirements and CV text in session state
                # st.session_state["cv_text"] = cv_text
                # st.session_state["requirements_input"] = requirements_input

            except Exception as e:
                st.error(f"Error extracting requirements: {e}")
        else:
            st.error("Please upload both the CV and the requirements matrix files.")


    # Display extracted requirements for user confirmation or modification
    st.subheader("Extracted Requirements:")
    requirements_input = st.text_area(
        "Please confirm or modify the extracted requirements: (editing this doesn't currently work due to some bug..)",
        value=formatted_requirements,
        height=300,
        key="keyRequirementsInput",
    )

    if st.button("Confirm and Fill Requirements Matrix"):
        try:
            # Get confirmed/modified requirements
            # confirmed_requirements = st.session_state["requirements_input"]
            confirmed_requirements = requirements_input
            # cv_text = st.session_state["cv_text"]
            # Extract text from CV PDF
            cv_text = document_utils.extract_text_from_pdf(cv_file)

            st.text(confirmed_requirements)

            # Combine all requirements into one prompt
            combined_requirements = f"{user_prompt}\n\n{confirmed_requirements}"

            with st.spinner("Filling requirements matrix..."):
                filled_response = matrices.fill_requirement_with_openai(
                    cv=cv_text,
                    requirement=combined_requirements,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt
                )

            st.subheader("Filled Requirements Matrix:")
            st.text_area("Filled Requirements", value=filled_response, height=300)
        except Exception as e:
            st.error(f"Error filling requirements matrix: {e}")

if __name__ == "__main__":
    main()

# To run the Streamlit app, use the following command:
# streamlit run src/summarizer/apps/streamlit_matrices_app.py