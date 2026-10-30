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
prompt = "suggest me name for my food company , suggest one name only"



# SYSTEM
message_system = {
    "role":"system",
    "content":"You are a food company name suggester"
}

message = {
    "role": role,
    "content": prompt
}
messages = [message_system , message]



#TEMPERATURE
response = client.chat.completions.create(model=model , messages=messages , temperature=0)
# print(response)

print("####################################################3")

answer = response.choices[0].message.content
print(answer)

