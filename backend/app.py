
from fastapi import FastAPI
from pydantic import BaseModel



app = FastAPI()

# run fastapi project:  uvicorn app:app --reload  

# app -> file name -> app.py
# app: fastapi object

# receive data -> connect with ai -> work flow -> return response

# create api -> for every task

# method -> api path -> data

@app.get("/")
def index():
    print("server running")
    return { "result": "success", "data": {}, "message": "Server running" }


@app.get("/get-llms") # api path
def get_llms():
    return { "result": "success", "message": "ok", "data": ["claude", "openai"]}

# courses, expereince, country

# name, email, password

class Signup(BaseModel):
    name: str
    email: str
    password: str

@app.post("/signup")
def signup(signup: Signup):
    return { "result": "success", "message": "account created succesfully", "data": signup }
    # insert into users(`name`, `email`, `pword`) values ('Bhavitya', 'contact@bhavitya.ai', '12345678'  ); 


class ChatData(BaseModel):
    business_id: str
    conversation_id: str
    message: str
    session_id: str
    timezone: str


@app.post("/api/wa/chat")
def ai_chat(chat_data: ChatData):
    print( chat_data.business_id)
    return { "result": "success", 'message': "our team will get back to you", "data": chat_data }




