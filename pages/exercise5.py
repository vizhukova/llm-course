import streamlit as st
import json
from openai import OpenAI
from env import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

with st.expander("See explanation"):
    st.markdown('''
    Write a prompt to generate 10 scenario based MCQ questions on Programming fundamentals
    using Python and validate the generated data.
    - 3 Simple questions.
    - 3 Medium questions
    - 4 Complex questions
    **Question Format:**
    - Question No Starts from 1 to 10
    - Complexity Level - Simple / Medium / Complex
    - Senario - Scenario that explain the real-time situation.
    - Question - Question based on the senario
    - Options and mark the correct option with a ‘+’ sign
     Explanation for the answer
                
    In the context of the scenario, Python is a versatile and widely-used programming language that
    is well-suited for web development. It offers simplicity, readability, and extensive libraries,
    making it an excellent choice for handling diverse tasks in the described project.
    ''')

def generate_mcqs(theme_input):
    """Generate MCQ questions using Generative AI with strict JSON format."""
    prompt = (
        f"""
        Generate 10 scenario based MCQ questions on {theme_input}:
        3 - Simple questions
        3 - Medium questions
        4 - Complex questions
        Question Format:
        Question No Starts from 1 to 10
        Complexity Level - Simple / Medium / Complex
        Senario - Scenario that explain the real-time situation.
        Question - Question based on the senario
        Options and mark the correct option with a ‘+’ sign
        Explanation for the answer
        GEnerate it in a markdown format.
        """
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that generates valid JSON MCQs."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        st.error(f"Error generating questions: {e}")
        return None

def validate_mcqs(mcqs):
    response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that verifying the json of MCQs."},
                {"role": "user", "content": mcqs}
            ],
            temperature=0.7
        )
    return response.choices[0].message.content

st.title("MCQ Question Generator")

theme_input = st.text_input('Write the theme that you want to generate MCQs for:', 'Python Fundamentals')
if st.button("Generate MCQs"):
    mcq_output = generate_mcqs(theme_input)
    validation_space = st.text('')
    st.markdown(mcq_output)
    if mcq_output:
        validation = validate_mcqs(mcq_output)
        print(validation)
        validation_space.write(validation)

