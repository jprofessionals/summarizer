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

    # Text input for system and user prompts
    system_prompt = st.text_area(
        "System Prompt",
        value=openai_utils.dict_roles["system"],
        height=150
    )

    user_prompt = st.text_area(
        "User Prompt",
        value=openai_utils.dict_roles["user"],
        height=150
    )

    # File upload
    uploaded_files = st.file_uploader(
        "Upload job listing documents (PDF, DOCX, or TXT)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if uploaded_files:
        all_text = ""
        for uploaded_file in uploaded_files:
            try:
                if uploaded_file.type == "application/pdf":
                    text = document_utils.extract_text_from_pdf(uploaded_file)
                elif uploaded_file.type == "text/plain":
                    text = document_utils.extract_text_from_txt(uploaded_file)
                elif (
                    uploaded_file.type
                    == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                ):
                    text = document_utils.extract_text_from_docx(uploaded_file)
                else:
                    st.error(f"Unsupported file type: {uploaded_file.type}")
                    continue

                all_text += text + "\n"
            except Exception as e:
                st.error(f"Error extracting text from file {uploaded_file.name}: {e}")

        if all_text:
            st.subheader("Extracted Text:")
            st.text_area("Job Listing Text", value=all_text, height=300)

            if st.button("Summarize"):
                with st.spinner("Generating summary..."):
                    try:
                        summary = openai_utils.summarize_text_with_openai(all_text, system_prompt, user_prompt)
                        st.subheader("Summary:")
                        st.write(summary)
                    except Exception as e:
                        st.error(f"Error generating summary: {e}")
        else:
            st.error("Unable to extract text from the documents. Please try other files.")

if __name__ == "__main__":
    main()

# To run the Streamlit app, use the following command:
# streamlit run src/summarizer/apps/streamlit_app.py