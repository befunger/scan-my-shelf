'''Utilities for using the ChatGPT API'''
import openai   # For ChatGPT access
import json     # For json handling

with open("C:/Projects/scan-my-shelf/API/openai.txt", 'r') as f:
    openai.api_key = f.read()

def format_prompt(extracted_text):
    '''Formats a ready prompt from the extracted text'''
    GPT_GET_BOOKS_PROMPT = f'''Extract all book titles from the following extracted text from an image. Only include real book titles.
    
    Extracted text: {extracted_text}

    Format: {{"books": ['book_1', 'book_2']}}
    '''

    return GPT_GET_BOOKS_PROMPT

def get_gpt_response(extracted_text: str,
                     model_name: str="gpt-3.5-turbo"
                     ) -> str:
    '''Get responses from an OpenAI LLM model for given queries'''

    gpt_input = format_prompt(extracted_text)

    completion = openai.ChatCompletion.create(
        model = model_name,
        messages=[
            {"role": "system", "content": "Output only valid JSON"},
            {"role": "user", "content": gpt_input}
        ],
        temperature = 0.7
    )

    text = completion.choices[0].message.content
    # print(text)
    parsed = json.loads(text)

    return parsed
