import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Api error")

client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-20b"


def llm_ans(prompt):
    message={
        "role": "user",
        "content" : prompt
    }
    messages = [message]
    response = client.chat.completions.create(model=model , messages=messages)
    ans = response.choices[0].message.content
    return ans

#BAD PROMPT
bad_prompt = """
This is a user complaint:
my laptop is not working 
classify this 
"""

bad_prompt2 = """
#ROLE
You are a support assistannt at a mobile/laptop company.

#TASK
You have to classify the issue in a category

#constraints
You have to classify the issue in one of the 3 categories namely billing , technical , return

#Output_Format
your answer should be in one word only and that one word should be one of the categories given in constraints.

#example(One shot)
For instance if a user complain says he wants a refund then the category is refund.

#FALLBACK
If the issue is unrelated to any of the categories mentioned in the constraints then the answer should be other

This is user complaint:
My laptop is not working.
"""

print(llm_ans(bad_prompt2))