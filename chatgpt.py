'''Utilities for using the ChatGPT API'''
import json     # For json handling
import openai   # For ChatGPT access

with open("C:/Projects/scan-my-shelf/API/openai.txt", 'r') as f:
    openai.api_key = f.read()

def format_prompt_1(extracted_text):
    '''Formats a ready prompt from the extracted text'''
    GPT_GET_BOOKS_PROMPT = f'''Extract the book title from the following extracted text from an image. The text may contain typos as well as garbage. Only include real book titles. Include only 1 title.
    
    Extracted text: {extracted_text}

    Format: {{"books": ['book']}}
    '''

    return GPT_GET_BOOKS_PROMPT

def format_single_prompt(extracted_text):
    '''Formats prompt for detecting single book'''

    GPT_GET_BOOKS_PROMPT = f'''Extract the book title from the following extracted text from an image. The text may contain typos as well as garbage. Only include real book titles. Include the author of the book.
    
    Extracted text: {extracted_text}

    Format: {{"book": ['book'], "author": ['author']}}
    '''
    return GPT_GET_BOOKS_PROMPT

def format_multi_prompt(extracted_text):
    '''Formats prompt for detecting multiple books'''

    GPT_GET_BOOKS_PROMPT = f'''Extract the book titles from the following extracted text from an image. The text may contain typos as well as garbage. Only include real book titles. Include the authors of the books.
        
    Extracted text: {extracted_text}

    Format: {{"book": ['book_1', 'book_2'], "author": ['author_1', 'author_2']}}
    '''
    return GPT_GET_BOOKS_PROMPT


def get_titles_from_text(extracted_text: str,
                        multi_detect: bool=False,
                        model_name: str="gpt-3.5-turbo-instruct"
                        ) -> str:
    '''Get responses from an OpenAI LLM model for given queries'''

    if multi_detect:
        gpt_input = format_multi_prompt(extracted_text)
    else:
        gpt_input = format_single_prompt(extracted_text)

    completion = openai.ChatCompletion.create(
        model = model_name,
        messages=[
            {"role": "system", "content": "Output only valid JSON"},
            {"role": "user", "content": gpt_input}
        ],
        temperature = 0.1
    )

    text = completion.choices[0].message.content
    # print(text)
    parsed = json.loads(text)

    return parsed
