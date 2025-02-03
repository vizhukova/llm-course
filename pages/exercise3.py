
import streamlit as st
from libs.mistralai import generate_text as mistralai_generate_text
from libs.deepseek import generate_text as deepseek_ai_generate_text

with st.expander("See explanation"):
    st.markdown('''
    **Objective:**  
    - Your objective is to create a chatbot or an application that acts as a Language Learning
    Assistant.
    - This AI tutor should help learners with vocabulary, pronunciation, grammar, and
    conversation
    practice in the target language.
    - It should offer personalized guidance and exercises to enhance language proficiency.  

    **Project Requirements:**  
    Select a Language: Choose a specific foreign language that the Language Learning Assistant will
    focus on  
    (e.g., Spanish, Mandarin, French).  
    User Interaction: Design a user-friendly interface for interacting with the Language Learning
    Assistant.  
    This could be a chatbot, mobile app, or web application that allows users to practice, learn, and
    receive feedback.  
    Content and Exercises: Integrate an AI model to provide language exercises, vocabulary lessons,
    pronunciation feedback, and conversation practice. The AI should tailor exercises to the user's
    skill level and offer constructive feedback.    
    ''')

st.title("Language Learning Assistant")

deepseek, mistral = model_options = ("deepseek-ai/DeepSeek-R1", "mistralai/Mistral-7B-Instruct-v0.2")
model_option = st.selectbox("What model would you like to use?", model_options)

def prompt_instruction(user_prompt: str) -> str:
    return f"""You are a helpful assistant, your goal is to be a tutor for the user and help him to
    learn the chosen language. You need to provide language exercises, vocabulary lessons,
    pronunciation feedback, and conversation practice. You should tailor exercises to the user's
    skill level and offer constructive feedback.
    
    Here is the user request: {user_prompt}
    """

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": """What is your target language, 
                    and what specific aspect would you like to focus on first:
                    vocabulary, pronunciation, grammar, or conversation skills?"""
    }]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What you want to know?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    generate_text = mistralai_generate_text if model_option == mistral else deepseek_ai_generate_text
    response = generate_text(
        prompt_instruction(prompt)
    )
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})