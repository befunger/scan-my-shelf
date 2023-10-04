'''Utilities for using the ChatGPT API'''
import json     # For json handling
import openai   # For ChatGPT access

with open("C:/Projects/scan-my-shelf/API/openai.txt", 'r', encoding="utf-8") as f:
    openai.api_key = f.read()

def format_single_prompt(extracted_text):
    '''Formats prompt for detecting single book'''

    gpt_get_books_prompt = f'''Extract the book title from the following extracted text from an image. The text may contain typos as well as garbage. Only include real book titles. Include the author of the book.
    
    Extracted text: {extracted_text}

    Format: {{"book": ['book'], "author": ['author']}}
    '''
    return gpt_get_books_prompt

def format_multi_prompt(extracted_text):
    '''Formats prompt for detecting multiple books'''

    gpt_get_books_prompt = f'''Extract the book titles from the following extracted text from an image. The text may contain typos as well as garbage. Only include real book titles. Include the authors of the books.
        
    Extracted text: {extracted_text}

    Format: {{"book": ['book_1', 'book_2'], "author": ['author_1', 'author_2']}}
    '''
    return gpt_get_books_prompt

def get_titles_from_text(extracted_text: str,
                        multi_detect: bool=False,
                        model_name: str="gpt-3.5-turbo"
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
    parsed = json.loads(text)

    return parsed

def verify_book(book_text: str,
                model_name: str="gpt-3.5-turbo"
                ) -> bool:
    '''Verify book title-author pair using OpenAI LLM model'''

    completion = openai.ChatCompletion.create(
        model = model_name,
        messages=[
            {"role": "system", "content": "You are a library assistant who provides accurate knowledge on books. Users will provide an author and book title and you respond True or False depending on if the book exists. Input is always of format 'Title, Author'. Output only True or False."},
            {"role": "user", "content": book_text}
        ],
        temperature = 0.1
    )

    output = completion.choices[0].message.content

    # return output == 'True'
    if output == 'True':
        print(f"TRUE: {book_text} matches.")
        return True

    if output == 'False':
        print(f"FALSE: {book_text} was rejected.")
        return False

    # This should never happen
    print(f"Output format mismatch. Input: {book_text}\nOutput: {output}")
    return False
