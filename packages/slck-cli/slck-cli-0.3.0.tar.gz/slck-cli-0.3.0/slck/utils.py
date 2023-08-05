import os
import sys
from typing import Dict, Optional

import dotenv


def get_token() -> str:
    dotenv.load_dotenv(override=True)
    token: Optional[str] = os.getenv("SLACK_BOT_TOKEN")
    if token is None:
        raise KeyError("SLACK_BOT_TOKEN is not found.")
    return token


def confirm_user_input(
    question: str, default: str = "yes", answer: Optional[str] = None
) -> bool:
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid: Dict[str, bool] = {
        "yes": True,
        "y": True,
        "ye": True,
        "no": False,
        "n": False,
    }
    prompt: str = " [y/n] "
    if default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice: str = input().lower() if answer is None else answer
        if choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")
