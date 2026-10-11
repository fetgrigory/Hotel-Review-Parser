import emoji


def remove_emoji(text: str) -> str:
    return emoji.replace_emoji(text, replace='')
