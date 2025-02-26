import json
import streamlit as st
from openai import OpenAI
from env import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

if "answers" not in st.session_state:
    st.session_state.answers = []
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "story_json" not in st.session_state:
    st.session_state.story_json = []

prompt = """
You are a master storyteller crafting a captivating mystery featuring a time-traveling detective. 
Your task is to weave an enthralling short story filled with suspense, clever deductions, and 
the mind-bending consequences of altering time. 
Follow these guidelines to ensure a gripping and immersive tale:
 The protagonist is a time-traveling detective with a distinct personality, skills, and a
compelling reason for utilizing time travel in solving mysteries.
- Develop a plot that involves a complex and intriguing mystery, taking advantage of
the
temporal aspect to add twists, turns, or unexpected connections.
- Create a vivid setting that seamlessly integrates different time periods, adding depth
and
richness to the narrative.
- Ensure that the story has a clear beginning, middle, and end, with a resolution to the
mystery that is both satisfying and unexpected.
- Encourage the model to incorporate elements of suspense, clever detective work, and
the
consequences of time travel on the detective's personal life or the overall investigation.
The format of response:
[{
"qestion": "Question here",
"options": ["Option 1", "Option 2", "Option 3", "Option 4"],
},
{
"qestion": "Question here",
"options": ["Option 1", "Option 2", "Option 3", "Option 4"],
},
...]
"""
answers = []
question_obj = None

with st.expander("See explanation"):
    st.markdown('''
    Compose a prompt that directs the language model to generate a short story with the following
    **Elements:**
    - The protagonist is a time-traveling detective with a distinct personality, skills, and a
    compelling reason for utilizing time travel in solving mysteries.
    - Develop a plot that involves a complex and intriguing mystery, taking advantage of
    the
    temporal aspect to add twists, turns, or unexpected connections.
    - Create a vivid setting that seamlessly integrates different time periods, adding depth
    and
    richness to the narrative.
    - Ensure that the story has a clear beginning, middle, and end, with a resolution to the
    mystery that is both satisfying and unexpected.
    - Encourage the model to incorporate elements of suspense, clever detective work, and
    the
    consequences of time travel on the detective's personal life or the overall investigation.
    ''')

if st.button("Start Story"):
    st.session_state.answers = []
    st.session_state.current_question = None
    st.session_state.story_json = []
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI that generates valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    story_json = json.loads(response.choices[0].message.content)
    st.session_state.story_json = story_json
    st.session_state.current_question = 0

if (
    st.session_state.current_question != None and
    len(st.session_state.story_json) > st.session_state.current_question and 
    st.session_state.story_json[st.session_state.current_question]):
    index = st.session_state.current_question 
    question_obj = st.session_state.story_json[index]
    answer = st.radio(
        f"**{index+1}.Question:** {question_obj['question']}", 
        question_obj['options'], 
        key=f"question_{index}"
    )
    if st.button("Next", key=f"next_question_{index}"):
        st.session_state.answers.append(f"{question_obj['question']} Answer: {answer}")
        st.session_state.current_question += 1
        st.rerun()

if st.session_state.current_question == len(st.session_state.story_json):
    with st.expander("Your Answers:"):
        st.markdown("\n".join(f"- {item}" for item in st.session_state.answers))

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI that generates a detective story with the usage of the provided answers on questions."},
            {"role": "user", "content": " ".join(f"{answer}." for answer in st.session_state.answers) }
        ],
        temperature=0.7
    )
    final_story = response.choices[0].message.content
    st.header("Here is your story:")
    st.write(final_story)
