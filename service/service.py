from data.questions import test_questions, diagnostic_questions


def get_next_test_question():
    for question in test_questions:
        yield question


def get_next_diagnostic_question():
    for question_pair in diagnostic_questions:
        yield question_pair[0]
        yield question_pair[1]
