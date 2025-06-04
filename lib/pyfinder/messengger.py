from inquirer import List, Checkbox, prompt, Confirm


def ask_terminal(message: str, type: str, choices: list = None):  # type: ignore
    if type != "confirm" and choices is None:
        raise ValueError("choices must be provided for this type")
    match type:
        case "list":
            question = [
                List(
                    "results",
                    message=message,
                    choices=list(choices),
                ),
            ]

        case "checkbox":
            question = [
                Checkbox(
                    "results",
                    message=message,
                    choices=list(choices),
                ),
            ]

        case "confirm":
            question = [
                Confirm(
                    "results",
                    message=message,
                ),
            ]
    answer = prompt(question)
    return answer["results"]  # type: ignore
