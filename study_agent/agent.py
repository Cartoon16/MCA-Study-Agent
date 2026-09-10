from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
from tools import calculate_minutes, check_answer

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("🎓 MCA Study Agent")
print("------------------")

subject = input("Enter subject: ")
topic = input("Enter topic: ")
time = int(input("How many minutes do you have? "))

prompt = f"""
You are an MCA Study Agent.

The student wants to study:
Subject: {subject}
Topic: {topic}
Available time: {time} minutes.

Your job is to create a practical study session.

First divide the available time into 4 study blocks.
Use the calculate_minutes tool to calculate the minutes per block.

Then provide:

1. What to learn first
2. Time allocation
3. One simple example
4. Three practice questions
5. A short revision task
6. Create a 3-question mini quiz.

For each question, use this exact format:

QUESTION: <question>
ANSWER: <correct answer>
EXPLANATION: <short explanation>

Create exactly 3 questions.
Do not number them.
Do not add extra text between questions.
Do not make the quiz too difficult.
"""

config = types.GenerateContentConfig(
    tools=[calculate_minutes, check_answer]
)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt,
    config=config
)

print("\n🤖 Study Agent:")
print(response.text)

quiz_text = response.text

questions = []
current_question = None
current_answer = None

for line in quiz_text.splitlines():
    line = line.strip()

    if line.startswith("QUESTION:"):
        current_question = line.replace("QUESTION:", "").strip()

    elif line.startswith("ANSWER:"):
        current_answer = line.replace("ANSWER:", "").strip()

        if current_question and current_answer:
            questions.append((current_question, current_answer))
            current_question = None
            current_answer = None


print("\n📝 Mini Quiz")
print("------------------")

score = 0

for i, (question, correct_answer) in enumerate(questions[:3], start=1):
    print(f"\nQ{i}. {question}")
    student_answer = input("Your answer: ")

    result = check_answer(student_answer, correct_answer)

    if result == "Correct":
        print("✅ Correct!")
        score += 1
    else:
        print(f"❌ Incorrect. Correct answer: {correct_answer}")


print("\n📊 Quiz Result")
print("------------------")
print(f"Score: {score}/{min(3, len(questions))}")

if score == 3:
    print("🎯 Excellent! You are ready for the next level.")
elif score >= 2:
    print("👍 Good job! Revise the topic once more.")
else:
    print("📚 You should revise the topic before moving ahead.")

print("\n------------------")
print("🎯 Your Study Agent session is ready!")

print("\n🤖 Agent Recommendation")
print("------------------")

if score == 3:
    print("Excellent! Move to the next topic: Normalization.")
elif score == 2:
    print("Good progress! Revise ERD relationships and practice more questions.")
elif score == 1:
    print("Revise ERD concepts and cardinality before moving ahead.")
else:
    print("Start again with ERD basics: entities, attributes, relationships, and cardinality.")