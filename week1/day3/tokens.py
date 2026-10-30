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
role = "user"

#3Prompt
prompt1 = "Hi!"
prompt2 = "Explain tme travel in detain"
prompt3 = "Write 1000 word essay on ML"

prompts = [prompt1,prompt2,prompt3]
for prompt in prompts :
    message = {
    "role": role,
    "content": prompt
    }
    messages = [message]
    response = client.chat.completions.create(model=model , messages=messages , max_tokens=50)
    usage = response.usage
    print(f"Prompt:{prompt} --> Your Tokens: {usage.prompt_tokens} --> Completion tokens {usage.completion_tokens} --> Total tokens: {usage.prompt_tokens+usage.completion_tokens}")
# print(response)

print("####################################################3")

answer = response.choices[0].message.content
print(answer)

