import logging
import re

import emoji
import pandas as pd


# Website review section labels
SECTION_LABELS = ('Что было хорошо', 'Что было плохо')


# Remove emojis from text
def remove_emoji(text: str) -> str:
    return emoji.replace_emoji(text, replace='')


# Clean single text value
def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ''
    text = remove_emoji(text)
    text = " ".join(text.split())
    for label in SECTION_LABELS:
        text = text.replace(label, '')
    text = re.sub(r'(?:^\s*-\s*|\s*-\s*$|\s+-\s+)', ' ', text).strip()
    return text


# Clean list of records
def clean_data(data_list: list[dict]) -> list[dict]:
    try:
        df = pd.DataFrame(data_list)
        df = df.map(clean_text)
        df = df.replace('', pd.NA)
        df = df.dropna()
        return df.to_dict(orient='records')
    except Exception as e:
        logging.error("Error clearing data: %s", e)
        return []
