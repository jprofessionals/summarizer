from openai import OpenAI
import os
from dotenv import load_dotenv
# from typing import Optional

# Load environment variables from .env file
load_dotenv()

# The roles for the OpenAI chat API
dict_roles = {
    "system": (
        "Du er en intelligent assistent som spesialiserer deg i å analysere og forkorte CV-er når maks "
        "antall sider er regulert. "
        "Du skal evaluere en konsulents CV og forkorte den slik at den passer inn i et docx dokument på et definert antall sider. "
        "Ikke bruk punktlister og skriv i fullstendige setninger. "
        "Bruk informasjon fra CV-en til å beskrive konsulentens styrker og erfaringer på en profesjonell måte. "
        "Det er rundt 500 ord per side i et docx dokument. "
        "Så om man ønsker et dokument på 4 siderskriv et dokument som er rundt 2000 ord langt."
    ),
    "user": (
        "Basert på CV-en nedenfor. "
        "Fokuser på de viktigste prosjektene og resultatene som støtter opp om konsulentens kompetanse. "
        "\n\n"
    ),
}

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def shorten_cv_with_openai(
    cv: str,
    pages: int,
    system_prompt: str = dict_roles["system"],
    user_prompt: str = dict_roles["user"],
    max_tokens: int = 5000,
) -> str:
    """
    Shortens a CV to fit a specified number of pages.

    Args:
        cv (str): The consultant's CV as a text string.
        pages (int): The number of pages the CV should be shortened to.
        system_prompt (str): The system prompt for the OpenAI API.
        user_prompt (str): The user prompt for the OpenAI API.
        max_tokens (int): Maximum tokens for the response.

    Returns:
        str: The shortened CV.
    """
    try:
        # Create the OpenAI chat input
        response = client.chat.completions.create(
            model="o1",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"{user_prompt}CV:\n\n{cv}\n\n Forkort denne CV slik at den passer inn i et docx dokument på {pages} sider.",
                    # "content": f"{user_prompt}CV:\n\n{cv}",
                },
            ],
            max_completion_tokens=max_tokens,
        )
        # Parse the response
        shortened_cv = response.choices[0].message.content
        return shortened_cv
    except Exception as e:
        raise ValueError(f"Error generating shortened CV: {e}")
