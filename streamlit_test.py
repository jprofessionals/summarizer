# %%

import streamlit as st

# import openai
from openai import OpenAI
import os

from dotenv import load_dotenv
from summarizer import document_utils

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

# Set your OpenAI API key here
# openai.api_key = os.environ.get("OPENAI_API_KEY")

# %%


def summarize_text_with_openai(text, max_tokens=500):
    # prompt = f"Please summarize the following job listing:\n\n{text}"
    # response = openai.Completion.create(
    # response = client.chat.completions.create(
    #     engine="gpt-4",  ## engine="text-davinci-003",  # "gpt-3.5-turbo"
    #     prompt=prompt,
    #     max_tokens=200,
    #     temperature=0.7,
    # )
    response = client.chat.completions.create(
        # model="gpt-4",  #
        model="o1",  #
        # TODO: Make system/user message more specific to specific to summarization of developer skill requirements?
        # messages=[
        #     {
        #         "role": "system",
        #         # "content": "You are a helpful assistant skilled in summarizing documents.",
        #         "content": "You are a helpful assistant skilled in summarizing job listings.",
        #     },
        #     {
        #         "role": "user",
        #         # "content": f"Summarize the following document:\n\n{text}",
        #         "content": f"Summarize the following job listing so that a programmer can easily see what skills are reuqired to see if they are relevant for the job, and to get a taste of what the job could be like:\n\n{text}",
        #     },
        # ],
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant specialized in summarizing job listings for developers. "
                    "Your summaries should be concise, structured, and tailored for programmers. "
                    "List technologies, programming languages, frameworks, tools, and other key requirements "
                    "as bullet points whenever possible."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Summarize the following job listing to make it easier for a developer to determine if their skills "
                    f"match the requirements. Focus on clearly listing the technologies, programming languages, frameworks, "
                    f"and tools required for the role, as well as a brief description of the job responsibilities and "
                    f"highlights:\n\n{text}"
                ),
            },
        ],
        max_tokens=max_tokens,
        temperature=0.5,  # Adjust temperature for more/less creativity
    )
    summary = response.choices[0].message.content
    return summary


# %%
def main():
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
                    summary = summarize_text_with_openai(text)
                st.subheader("Summary:")
                st.write(summary)
        else:
            st.error(
                "Unable to extract text from the document. Please try another file."
            )


if __name__ == "__main__":
    main()


# streamlit run job_listing_summarizer.py --reload
