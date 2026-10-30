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

#STRUCTURE IT
from pydantic import BaseModel
class Ticket(BaseModel):
    name:str
    email:str
    issue:str

schema = Ticket.model_json_schema()

response_format ={
    "type": "json_object"
}

system_prompt = f"""
Extract the personal information from the ticket strictly based om this schema and give me a json output {schema}
"""
message_system = {
    "role":"system",
    "content" : system_prompt
}

text = "Hello,my name is saharsh. I have an iPhone which is not working at all . my address is vrindavan . My email is abc@gmail.com . My contact number is 75057 . I broke up with my gf yesterday and yesterday i went to delhi "
prompt = f"""
This is a coustomer ticket. please extract the personal informaation from this.{text} in json output
"""
message = {
    "role": role,
    "content": prompt
}
messages = [message_system , message]

response = client.chat.completions.create(model=model , messages=messages, response_format=response_format)

answer = response.choices[0].message.content
print(answer)

#isko padhte kaise hai ??
import json
raw_json = answer
data_files = json.loads(raw_json)
ticket = Ticket(**data_files)

#isko paas kar sakte hai aage !!!!!!!!
print(ticket.name)
print(ticket.email)
print(ticket.issue)