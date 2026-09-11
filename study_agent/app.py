import streamlit as st
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

from tools import calculate_minutes, check_answer


# Load API key
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


st.set_page_config(
    page_title="MCA Study Agent",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 MCA Study Agent")
st.write("Your AI-powered personalized study assistant")


# -----------------------------
# Student Input
# -----------------------------

st.sidebar.header("📚 Study Details")

subject = st.sidebar.text_input(
    "Subject",
    placeholder="Example: Database Management"
)

topic = st.sidebar.text_input(
    "Topic",
    placeholder="Example: ERD"
)

time = st.sidebar.number_input(
    "Available study time (minutes)",
    min_value=20,
    max_value=600,
    value=120,
    step=10
)


# -----------------------------
# Generate Study Plan
# -----------------------------

if st.sidebar.button("🚀 Generate Study Plan"):

    if not subject or not topic:
        st.warning("Please enter both subject and topic.")
    else:

        with st.spinner("🤖 Agent is preparing your study plan..."):

            prompt = f"""
You are an MCA Study Agent.

The student wants to study:

Subject: {subject}
Topic: {topic}
Available time: {time} minutes.

Create a practical personalized study session.

First divide the available time into 4 study blocks.
Use the calculate_minutes tool to calculate the minutes per block.

Provide:

1. What to learn first
2. Time allocation
3. One simple example
4. Three practice questions
5. A short revision task
6. A 3-question mini quiz

For each quiz question use EXACTLY this format:

QUESTION: <question>
ANSWER: <correct answer>
EXPLANATION: <short explanation>

Create exactly 3 quiz questions.

Keep everything suitable for an MCA beginner.
"""

            config = types.GenerateContentConfig(
                tools=[calculate_minutes]
            )

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
                config=config
            )

            st.session_state.study_plan = response.text


# -----------------------------
# Display Study Plan
# -----------------------------

if "study_plan" in st.session_state:

    st.subheader("📖 Your Personalized Study Plan")

    st.markdown(st.session_state.study_plan)

    quiz_text = st.session_state.study_plan

    questions = []
    current_question = None
    current_answer = None

    for line in quiz_text.splitlines():

        line = line.strip()

        if line.startswith("QUESTION:"):
            current_question = line.replace(
                "QUESTION:", ""
            ).strip()

        elif line.startswith("ANSWER:"):
            current_answer = line.replace(
                "ANSWER:", ""
            ).strip()

            if current_question and current_answer:
                questions.append(
                    (current_question, current_answer)
                )

                current_question = None
                current_answer = None

    st.session_state.questions = questions


# -----------------------------
# Quiz
# -----------------------------

if "questions" in st.session_state and st.session_state.questions:

    st.divider()

    st.subheader("📝 Mini Quiz")

    answers = []

    for i, (question, correct_answer) in enumerate(
        st.session_state.questions[:3],
        start=1
    ):

        st.write(f"### Q{i}. {question}")

        answer = st.text_input(
            f"Your answer for Q{i}",
            key=f"answer_{i}"
        )

        answers.append(
            (answer, correct_answer)
        )


    if st.button("✅ Submit Quiz"):

        score = 0

        for student_answer, correct_answer in answers:

            result = check_answer(
                student_answer,
                correct_answer
            )

            if result == "Correct":
                score += 1

        st.subheader("📊 Quiz Result")

        st.write(
            f"### Score: {score}/3"
        )

        if score == 3:

            st.success(
                "🎯 Excellent! You are ready for the next level."
            )

            st.info(
                "🤖 Agent Recommendation: Move to the next topic."
            )

        elif score == 2:

            st.info(
                "👍 Good job! Revise the topic once more."
            )

            st.info(
                "🤖 Agent Recommendation: Practice a few more questions."
            )

        else:

            st.warning(
                "📚 Revise the topic before moving ahead."
            )

            st.info(
                "🤖 Agent Recommendation: Review the basics and try the quiz again."
            )