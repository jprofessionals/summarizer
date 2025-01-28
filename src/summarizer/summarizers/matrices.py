from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# The roles for the OpenAI chat API
dict_roles = {
    "system": (
        "Du er en intelligent assistent som spesialiserer deg i å analysere CV-er og fylle ut krav lister for konsulenter. "
        "Du skal evaluere en konsulents erfaringer og resultater mot de spesifikke kravene. "
        "Bruk informasjon fra CV-en til å beskrive konsulentens styrker og erfaringer for hvert krav. "
        "Fyll ut matrisen på en strukturert måte, med konkrete eksempler fra CV-en."
    ),
    "user": (
        "Basert på CV-en og kravmatrisen som følger, analyser hvor godt konsulenten oppfyller hvert krav. "
        "For hvert punkt gi en beskrivelse av hvor godt konsulenten oppfyller dette kravet, prosjekter og resultater som støtter opp om kompetansen. "
        # "Hopp over de første punktene om personalia og annen generell administrativ informasjon som navn, kontaktinformasjon, timepris, etc. "
        "\n\n"
    )
}

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def fill_requirement_with_openai(
        cv: str,
        requirement: str,
        system_prompt: str = dict_roles["system"],
        user_prompt: str = dict_roles["user"],
        max_tokens: int = 5000) -> str:
    """
    Fills out a single requirement based on a consultant's CV.

    Args:
        cv (str): The consultant's CV as a text string.
        requirement (str): A single requirement to be fulfilled.
        system_prompt (str): The system prompt for the OpenAI API.
        user_prompt (str): The user prompt for the OpenAI API.
        max_tokens (int): Maximum tokens for the response.

    Returns:
        str: The response for the requirement.
    """
    try:
        # Create the OpenAI chat input
        response = client.chat.completions.create(
            model="o1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{user_prompt}CV:\n\n{cv}\n\nKrav:\n\n{requirement}"}
            ],
            max_completion_tokens=max_tokens,
        )
        # Parse the response
        filled_requirement = response.choices[0].message.content
        return filled_requirement
    except Exception as e:
        raise ValueError(f"Error generating response for requirement: {e}")