# %%

# import openai
from openai import OpenAI
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# %%

def summarize_text_with_openai(text, max_tokens=700) -> str:
    """
    Summarizes a given text using OpenAI's GPT-4 API.
    Args:
        text (str): The text to summarize.
        max_tokens (int): The maximum length of the summary.
    Returns:
        str: The summary of the text.
    """

    response = client.chat.completions.create(
        # model="gpt-4",  #
        model="o1",  #

        messages=[
            {
            "role": "system",
            "content": (
                "Du er en hjelpsom assistent spesialisert i å oppsummere jobbutlysninger for utviklere i et konsulentselskap. "
                "Oppsummeringene dine skal være korte, strukturerte og rettet mot utviklere. "
                "List opp teknologier, programmeringsspråk, rammeverk, verktøy og andre viktige krav "
                "som punktlister der det er mulig. Samt en kort beskrivelse av rolle, arbeidsgiver og lokasjon."
            )
            },
            {
            "role": "user",
            "content": (
                "Oppsummer følgende jobbannonse for å gjøre det enklere for en utvikler å vurdere om deres kompetanse "
                "passer til kravene. Fokuser på å tydelig liste opp teknologier, programmeringsspråk, rammeverk "
                "og verktøy som kreves for rollen, samt en kort beskrivelse av arbeidsoppgavene og "
                "viktige høydepunkter slik at utviklerene kan vurdere om utlysningen virker interessant."
                "Legg og ved en kort beskrivelse av rolle, arbeidsgiver og lokasjonen. "
                f"Jobb annonsen: \n\n{text}"
            )
            },
        ],
        # max_tokens=max_tokens, # Old version
        max_completion_tokens=max_tokens,
        # temperature=0.5,  # Adjust temperature for more/less creativity
    )
    summary = response.choices[0].message.content
    return summary
# %%
