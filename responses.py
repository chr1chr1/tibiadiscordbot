import tibiadata


def get_response(user_input: str, prev: str) -> str:
    return tibiadata.get_deaths(user_input.lower(), prev)