import streamlit as st

from summarizer import document_utils, openai_utils

def main() -> None:
    """
    Main function of the Streamlit app.
    """
    st.set_page_config(
        page_title="Job Listing Summarizer", 
        # layout="wide"
        )


    st.title("Job Listing Summarizer")

    # File upload
    uploaded_file = st.file_uploader(
        "Upload a job listing document (PDF or DOCX or TXT)",
        type=["pdf", "docx", "txt"],
    )

    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            text = document_utils.extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "text/plain":
            text = document_utils.extract_text_from_txt(uploaded_file)
        elif (
            uploaded_file.type
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            text = document_utils.extract_text_from_docx(uploaded_file)

        if text:
            st.subheader("Extracted Text:")
            st.text_area("Job Listing Text", value=text, height=300)

            if st.button("Summarize"):
                with st.spinner("Generating summary..."):
                    summary = openai_utils.summarize_text_with_openai(text)
                st.subheader("Summary:")
                st.write(summary)
        else:
            st.error(
                "Unable to extract text from the document. Please try another file."
            )


if __name__ == "__main__":
    main()

# streamlit run src/summarizer/apps/streamlit_app.py 
# streamlit run src/summarizer/apps/streamlit_app.py --reload

