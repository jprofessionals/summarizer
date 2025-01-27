import streamlit as st
from summarizer.summarizers import matrices

def main() -> None:
    """
    Main function of the Streamlit app for filling out requirements matrices.
    """
    st.set_page_config(
        page_title="Requirements Matrix Filler", 
        # layout="wide"
    )

    st.title("Requirements Matrix Filler")

    # Text input for system and user prompts
    system_prompt = st.text_area(
        "System Prompt",
        value=matrices.dict_roles["system"],
        height=150
    )

    user_prompt = st.text_area(
        "User Prompt",
        value=matrices.dict_roles["user"],
        height=150
    )

    # Text input for CV
    cv_text = st.text_area(
        "Consultant's CV",
        height=300
    )

    # Text input for requirements matrix
    requirements_text = st.text_area(
        "Requirements Matrix (in JSON format)",
        height=300
    )

    if st.button("Fill Requirements Matrix"):
        try:
            requirements = eval(requirements_text)  # Convert the input text to a dictionary
            with st.spinner("Filling requirements matrix..."):
                filled_matrix = matrices.fill_requirements_matrix_with_openai(
                    cv=cv_text,
                    requirements=requirements,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt
                )
            st.subheader("Filled Requirements Matrix:")
            st.json(filled_matrix)
        except Exception as e:
            st.error(f"Error filling requirements matrix: {e}")

if __name__ == "__main__":
    main()

# To run the Streamlit app, use the following command:
# streamlit run src/summarizer/apps/streamlit_matrices_app.py