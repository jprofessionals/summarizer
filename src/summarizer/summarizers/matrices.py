from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# The roles for the OpenAI chat API
dict_roles = {
    "system": (
        "Du er en intelligent assistent som spesialiserer deg i å analysere CV-er og fylle ut kravmatriser for konsulenter. "
        "Du skal evaluere en konsulents erfaringer og resultater mot en spesifikk kravmatrise. "
        "Bruk informasjon fra CV-en til å beskrive konsulentens styrker og erfaringer for hvert krav i matrisen. "
        "Fyll ut matrisen på en strukturert måte, med konkrete eksempler fra CV-en."
    ),
    "user": (
        "Basert på CV-en nedenfor og kravmatrisen som følger, analyser hvor godt konsulenten oppfyller hvert krav. "
        "For hvert punkt i matrisen gi en beskrivelse av hvor godt konsulenten oppfyller dette kravet, prosjekter og resultater som støtter opp om kompetansen. "
        "\n\n"
    )
}

# Intialize the OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def fill_requirements_matrix_with_openai(
        cv: str,
        requirements: dict,
        system_prompt: str = dict_roles["system"],
        user_prompt: str = dict_roles["user"],
        max_tokens: int = 2000) -> dict:
    """
    Fills out a requirements matrix based on a consultant's CV.

    Args:
        cv (str): The consultant's CV as a text string.
        requirements (dict): A dictionary representing the requirements matrix.
        max_tokens (int): Maximum tokens for the response.

    Returns:
        dict: The filled requirements matrix.
    """
    try:
        # Format requirements into a readable prompt
        requirements_text = "\n".join([f"{key}: {value}" for key, value in requirements.items()])

        # Create the OpenAI chat input
        response = client.chat.completions.create(
            # model="gpt-4",
            model="o1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{user_prompt}CV:\n\n{cv}\n\nKravmatrise:\n\n{requirements_text}"}
            ],
            max_completion_tokens=max_tokens,
        )
        # Parse the response into a dictionary format (or keep it as text)
        filled_matrix = response.choices[0].message.content
    except Exception as e:
        raise ValueError(f"Error processing requirements matrix: {e}")
    
    return filled_matrix
