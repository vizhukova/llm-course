
import streamlit as st
from libs.mistralai import generate_text as mistralai_generate_text
from libs.deepseek import generate_text as deepseek_ai_generate_text
from libs.llama import generate_text as llama_generate_text

with st.expander("See explanation"):
    st.markdown('''
    **Objective:**  
    Your objective is to build a chatbot that behaves like a tutor. This chatbot should engage in
    conversations with users, ask probing questions, and guide them towards a deeper understanding
    of a specific topic or problem. The chatbot should not provide direct answers; instead, it should
    encourage critical thinking and self-discovery.  

    **Project Requirements:**  
    Select a Domain: Choose a specific domain or topic that the chatbot will focus on.  
    (e.g., mathematics, philosophy, science, literature).  
    User Interaction: Design a user-friendly interface for interacting with the chatbot. This could be a
    web application, mobile app, or a simple text-based chat interface.  
    Dialog Flow: Develop a conversation flow that initiates with the user's questions or topics and
    gradually guides the conversation using the Socratic method. The chatbot should be able to
    understand and respond to natural language inputs.  
    Question Generation: Integrate OpenAI's language models (GPT-3 or a more recent version if
    available) to generate insightful questions and responses. The chatbot should ask questions to
    help users think critically about the topic and reach their own conclusions.    
    ''')

st.title("Learning Tutor Chatbot")

llama, deepseek, mistral = model_options = (
    "meta-llama/Llama-3.3-70B-Instruct", 
    "deepseek-ai/DeepSeek-R1", 
    "mistralai/Mistral-7B-Instruct-v0.2"
    )
model_option = st.selectbox("What model would you like to use?", model_options)

def prompt_instruction(user_prompt: str) -> str:
    messages_history = "\n".join(f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages)
    
    return f"""You are a helpful assistant, your goal is to be a tutor for the user and help him to
    learn thechosen topic. You should engage in conversations with users, ask probing questions, 
    and guide them towards a deeper understanding of a specific topic or problem. 
    The chatbot should not provide direct answers; instead, it should encourage critical thinking 
    and self-discovery.

    Use the hostory conversation to guide the user. Here is the conversation history:
    {messages_history}
    
    Here is the user request: {user_prompt}
    """

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": """What is the specific domain or topic that the you want to focus on
                    (e.g., mathematics, philosophy, science, literature)?
                   """
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

    if model_option == mistral:
        generate_text = mistralai_generate_text
    elif model_option == deepseek:
        generate_text = deepseek_ai_generate_text
    else:
        generate_text = llama_generate_text

    response = generate_text(
        prompt_instruction(prompt)
    )
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})