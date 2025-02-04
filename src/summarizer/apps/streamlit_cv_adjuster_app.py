import streamlit as st
from summarizer import document_utils

# from summarizer.summarizers import matrices
from summarizer.summarizers import cv_adjuster
# from typing import Optional


def main() -> None:
    """
    Main function of the Streamlit app for shortening CVs.
    """
    st.set_page_config(
        page_title="CV Shortener",
        # layout="wide"
    )

    st.title("CV Shortener")

    # Text input for system and user prompts
    system_prompt = st.text_area(
        "System Prompt", value=cv_adjuster.dict_roles["system"], height=150
    )

    user_prompt = st.text_area(
        "User Prompt", value=cv_adjuster.dict_roles["user"], height=150
    )

    # File upload for CV (PDF)
    cv_file = st.file_uploader("Upload Consultant's CV (PDF)", type=["pdf"])

    # Number input for the number of pages
    pages = st.number_input("Number of Pages", min_value=1, max_value=10, value=2)

    if st.button("Shorten CV"):
        if cv_file:
            try:
                # Extract text from CV PDF
                cv_text = document_utils.extract_text_from_pdf(cv_file)

                # Shorten the CV using the cv_adjuster module
                shortened_cv = cv_adjuster.shorten_cv_with_openai(
                    cv=cv_text,
                    pages=pages,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                )

                # Display the shortened CV
                st.subheader("Shortened CV:")
                st.text_area("Shortened CV", value=shortened_cv, height=300)

            except Exception as e:
                st.error(f"Error shortening CV: {e}")
        else:
            st.error("Please upload a CV file.")


if __name__ == "__main__":
    main()

# To run the Streamlit app, use the following command:
# streamlit run src/summarizer/apps/streamlit_cv_adjuster_app.py
