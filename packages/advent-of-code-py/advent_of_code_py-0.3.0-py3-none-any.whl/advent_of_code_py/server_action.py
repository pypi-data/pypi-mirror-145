"""module which performs server realted actions such as submitting and downloading"""
import requests

from .cache_file import (
    check_if_downloaded,
    check_less_than_one_min_submission,
    last_submitted_answer_message,
    save_input_to_location,
    save_last_submission_time,
    save_submitted_answer,
)
from .config_file import get_session_value

INPUT_URL = "https://adventofcode.com/{}/day/{}/input"
SUBMIT_URL = "https://adventofcode.com/{}/day/{}/answer"


def download_input(year: int, day: int, session: str):
    """Download file from a advent of code server and save it for future reference"""
    session_value = get_session_value(session)
    if not check_if_downloaded(year, day, session):
        input_url = INPUT_URL.format(year, day)
        html_data = requests.get(input_url, cookies={"session": session_value})
        save_input_to_location(year, day, session, html_data.text)


def submit_output(year: int, day: int, part: int, session: str, output: str) -> str:
    """Submit solution output to a advent of code server"""
    session_value = get_session_value(session)
    submit_url = SUBMIT_URL.format(year, day)
    submitted_message = last_submitted_answer_message(year, day, part, session, output)
    if not submitted_message:
        early_submission = check_less_than_one_min_submission(year, day, session)
        if early_submission:
            message = "You have to wait for 1 min before submitting next solution"
        else:
            data = {"level": part, "answer": output}
            save_last_submission_time(year, day, session)
            response = requests.post(
                submit_url, data, cookies={"session": session_value}
            )
            if response.status_code != 200:
                message = (
                    "Error submiting solution online. Returned non 200 status code"
                )
            else:
                text_data = response.text
                if "too high" in text_data:
                    message = "Your answer is too high"
                    save_submitted_answer(year, day, part, session, output, message)
                elif "too low" in text_data:
                    message = "Your answer is too low"
                    save_submitted_answer(year, day, part, session, output, message)
                elif "That's not" in text_data:
                    message = "That's not the right answer"
                    save_submitted_answer(year, day, part, session, output, message)
                elif "You don't seem" in text_data:
                    message = "You don't seem to be solving right level"
                elif "You gave an answer" in text_data:
                    message = (
                        "You have to wait for 1 min before submitting next solution"
                    )
                elif "That's the right answer" in text_data:
                    message = "Congratulation, you have solved question successfully"
                    save_submitted_answer(
                        year,
                        day,
                        part,
                        session,
                        output,
                        "Congratulation, you have solved question correctly",
                    )
                else:
                    message = (
                        "Got unknown message. Please retry if answered is not submitted"
                    )
        return message
    return submitted_message
