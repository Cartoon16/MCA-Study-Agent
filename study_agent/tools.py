def calculate_minutes(total_minutes: int, topics: int) -> int:
    """Divide total study minutes equally among topics."""
    return total_minutes // topics


def check_answer(student_answer: str, correct_answer: str) -> str:
    """Check whether the student's answer matches the expected answer."""
    if student_answer.strip().lower() == correct_answer.strip().lower():
        return "Correct"
    return "Needs improvement"