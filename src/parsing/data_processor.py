import re

import emoji
import pandas as pd


# Remove emojis from text
def remove_emoji(text: str) -> str:
    return emoji.replace_emoji(text, replace='')


# Clean individual text from emojis, extra line breaks and garbage
def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ''
    text = remove_emoji(text)
    text = " ".join(text.split())
    text = text.replace('Что было хорошо', '').replace('Что было плохо', '')
    text = re.sub(r'\s+-\s+', ' ', text)
    text = re.sub(r'^-\s*', '', text)
    text = re.sub(r'\s*-$', '', text)
    text = re.sub(r'^-$', '', text)

    return text.strip()


# Batch data cleaning for a list of dictionaries
def clean_data(data_list: list[dict]) -> list[dict]:
    try:
        df = pd.DataFrame(data_list)
        df = df.dropna()
        df = df.replace('Что было хорошо', '', regex=True)
        df = df.replace('Что было плохо', '', regex=True)

        def remove_placeholder_dash(text):
            if isinstance(text, str):
                text = " ".join(text.split())
                text = re.sub(r'\s+-\s+', ' ', text)
                text = re.sub(r'^-\s*', '', text)
                text = re.sub(r'\s*-$', '', text)
                text = re.sub(r'^-$', '', text)
                return text.strip()
            return text

        df = df.map(remove_placeholder_dash)
        df = df.replace(r'^\s*$', pd.NA, regex=True)
        df = df.dropna()

        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Ошибка при очистке данных: {e}")
        return []
