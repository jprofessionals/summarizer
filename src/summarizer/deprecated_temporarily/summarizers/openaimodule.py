# %%
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key
# api_key = os.getenv('CHATGPT_API_KEY')
# print(api_key)

# Set your OpenAI API key

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)
# print(os.getenv('OPENAI_API_KEY'))


# %%


def summarize_document(document_text, max_tokens=150):
    """
    Summarizes a given document using OpenAI's GPT-3.5/4 API.

    Args:
        document_text (str): The text of the document to summarize.
        max_tokens (int): The maximum length of the summary.

    Returns:
        str: The summary of the document.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo" based on your plan
            # TODO: Make system/user message more specific to specific to summarization of developer skill requirements?
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant skilled in summarizing documents.",
                },
                {
                    "role": "user",
                    "content": f"Summarize the following document:\n\n{document_text}",
                },
            ],
            max_tokens=max_tokens,
            temperature=0.5,  # Adjust temperature for more/less creativity
        )
        # summary = response["choices"][0]["message"]["content"]
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        return f"An error occurred: {e}"


# %%

# Example usage
if __name__ == "__main__":
    # Example document
    document_text = """
    OpenAI is a research laboratory consisting of the for-profit OpenAI LP and its parent company, the non-profit OpenAI Inc.
    The company conducts research in the field of artificial intelligence (AI) with the declared intention of promoting and
    developing friendly AI in a way that benefits humanity as a whole. OpenAI was founded in December 2015 by Elon Musk,
    Sam Altman, and others, who collectively pledged $1 billion.
    """

    # Summarize the document
    summary = summarize_document(document_text)
    print("Summary:")
    # print(response.choices[0].message.content)
    print(summary)

# %%
