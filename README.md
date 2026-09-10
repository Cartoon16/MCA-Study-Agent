# 🎓 MCA Study Agent

An Agentic AI study assistant built using Python and Google Gemini.

The agent creates a personalized study plan based on the student's subject, topic, and available study time. It can use tools to divide study time, generate a quiz, evaluate answers, and provide an adaptive recommendation.

---

## 🚀 Features

- 📚 Personalized study plan
- ⏱️ Automatic study-time allocation
- 🛠️ Tool calling with Python functions
- 📝 Automatic 3-question mini quiz
- ✅ Automatic answer checking
- 📊 Quiz score calculation
- 🤖 Adaptive study recommendation

---

## 🧠 How It Works

The workflow is:

Student Input
↓
Gemini Study Agent
↓
calculate_minutes() Tool
↓
Personalized Study Plan
↓
AI Generated Quiz
↓
check_answer() Tool
↓
Quiz Score
↓
Adaptive Recommendation

---

## 🛠️ Technologies Used

- Python
- Google Gemini API
- Google GenAI SDK
- python-dotenv
- Function Calling / Tool Calling

---

## 📁 Project Structure

```text
Agentic/
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
│
├── venv/
│
└── study_agent/
    ├── agent.py
    └── tools.py