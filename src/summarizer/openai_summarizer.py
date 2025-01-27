from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# The roles for the OpenAI chat API
dict_roles = {
    "system": (
        "Du er en hjelpsom assistent spesialisert i å oppsummere jobbutlysninger for utviklere i et konsulentselskap. "
        "Oppsummeringene dine skal være korte, strukturerte og rettet mot utviklere. "
        "List opp teknologier, programmeringsspråk, rammeverk, verktøy og andre viktige krav "
        "som punktlister der det er mulig. Start med en punktliste med kort beskrivelse av rolle, arbeidsgiver og lokasjon."
    ),
    "user": (
        "Oppsummer følgende jobbannonse for å gjøre det enklere for en utvikler å vurdere om deres kompetanse "
        "passer til kravene. Fokuser på å tydelig liste opp teknologier, programmeringsspråk, rammeverk "
        "og verktøy som kreves for rollen, samt en kort beskrivelse av arbeidsoppgavene og "
        "viktige høydepunkter slik at utviklerene kan vurdere om utlysningen virker interessant. "
        "Jobb annonsen: \n\n"
    )
    }

# Retrieve the API key
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def summarize_text_with_openai(
        text: str, 
        system_prompt: str = dict_roles["system"], 
        user_prompt: str = dict_roles["user"], 
        max_tokens: int = 1000) -> str:
    """
    Summarizes a given text using OpenAI's GPT-4 API.

    Args:
        text (str): The text to summarize.
        max_tokens (int): The maximum length of the summary.

    Returns:
        str: The summary of the text.
    """
    try:
        response = client.chat.completions.create(
            model="o1",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                    # "content": (
                    #     "Du er en hjelpsom assistent spesialisert i å oppsummere jobbutlysninger for utviklere i et konsulentselskap. "
                    #     "Oppsummeringene dine skal være korte, strukturerte og rettet mot utviklere. "
                    #     "List opp teknologier, programmeringsspråk, rammeverk, verktøy og andre viktige krav "
                    #     "som punktlister der det er mulig. Start med en punktliste med kort beskrivelse av rolle, arbeidsgiver og lokasjon."
                    # )
                },
                {
                    "role": "user",
                    "content": user_prompt + text,
                    # "content": (
                    #     "Oppsummer følgende jobbannonse for å gjøre det enklere for en utvikler å vurdere om deres kompetanse "
                    #     "passer til kravene. Fokuser på å tydelig liste opp teknologier, programmeringsspråk, rammeverk "
                    #     "og verktøy som kreves for rollen, samt en kort beskrivelse av arbeidsoppgavene og "
                    #     "viktige høydepunkter slik at utviklerene kan vurdere om utlysningen virker interessant."
                    #     f"Jobb annonsen: \n\n{text}"
                    # )
                },
            ],
            max_completion_tokens=max_tokens,
        )
        summary = response.choices[0].message.content
    except Exception as e:
        raise ValueError(f"Error summarizing text with OpenAI: {e}")
    
    return summary