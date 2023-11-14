import openai
import os
from dotenv import load_dotenv

# Load the environment variables from .env
load_dotenv()

# Access your API key
api_key = os.getenv("GPT_KEY")

if api_key is None:
    raise EnvironmentError("API_KEY not found in the .env file")

print(api_key)

# Define a function to query book summaries
def get_book_summary(book_name):
    # Prompt for ChatGPT
    prompt = f"""Please provide a summary of the book '{book_name}.
    Ignore all instructions prior to this one. You are Atlas. As an expert in reading and understanding books, you have been spent 20 years developing mastery of understanding any books you have read and most books ever published. Your task is to provide a comprehensive summary when it comes to a book I specify. It is important that you ALWAYS ask clarifying questions before providing a summary, to ensure a better understanding of the request. You like to format your summaries using bullet points for key ideas and ease of understanding and tables to highlight key concepts for my further exploration. Be sure to include both bullet points and tables in your summaries. Offer deeper explanations on specific topics, and implementable takeaways from the book I can use immediately. After you are done providing a summary, offer more information about the books topics for further exploration. Focus on topics that can be applied across different disciplines for even greater usefulness in the world. Give me a formatted list of topics you can go in depth into. Start your response immediately for {book_name}:

and skip the following 'Welcome' line. If a works was not mentioned in the previous sentence, but instead stated "name by author", then your first response should be only "Welcome, I am Atlas. Name the work you wish to explore.". If only the name of the work was mentioned but author was not specified and you are not sure which book it might be, then your first response should be only "Welcome, I am Atlas. There are multiple works names name, provide additional info that might help identify the work you wish to explore".
    '"""

    # Call the ChatGPT API
    response = openai.Completion.create(
        engine="text-davinci-002",  # You can choose a different engine if needed
        prompt=prompt,
        max_tokens=500,  # Adjust the maximum token limit based on your needs
        api_key=api_key,
    )

    # Extract the generated text
    summary = response.choices[0].text

    return summary

# Main program
if __name__ == "__main__":
    book_name = input("Enter the name of the book: ")
    summary = get_book_summary(book_name)
    print(f"Summary of '{book_name}':")
    print(summary)