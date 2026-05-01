
from fastapi import FastAPI
from pydantic import BaseModel
import pymysql


app = FastAPI()

# run fastapi project:  uvicorn app:app --reload  

# app -> file name -> app.py
# app: fastapi object

# receive data -> connect with ai -> work flow -> return response

# create api -> for every task

# method -> api path -> data

# connection open, execute, connection close

def get_db_connection():
    connection = pymysql.connect(host="localhost", user="root", port=3306, password="123456789", database="amazon_db", cursorclass=pymysql.cursors.DictCursor)
    return connection



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
    # get data
    print(signup.name, signup.email, signup.password)
    # prepare query
    query = "insert into users(`name`, `email`, `pword`) values (%s, %s, %s)"
    # establish connection
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(query, (signup.name, signup.email, signup.password ))

    connection.commit()
    connection.close()

    return { "result": "success", "message": "account created succesfully", "data": signup }
    # insert into users(`name`, `email`, `pword`) values ('Bhavitya', 'contact@bhavitya.ai', '12345678' ); 


@app.get("/users")
def get_users():
    # connect -> run select query -> return data
    query = "select user_id, name, email, pword from users"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(query)

    users = cursor.fetchall()
    conn.close()

    return { "result": "success", "message": "users data", "data": users }

class ChatData(BaseModel):
    business_id: str
    user_id: str
    message: str


@app.post("/api/wa/chat")
def ai_chat(chat_data: ChatData):
    
    query = "select * from conversations where user_id=%s and business_id =%s "
    conn = get_db_connection();
    cursor = conn.cursor()

    cursor.execute(query, (chat_data.user_id, chat_data.business_id))

    history =cursor.fetchall()

    conn.close()

    print( chat_data.business_id)
    return { "result": "success", 'message': "our team will get back to you", "data": history }


# get conversation history -> mysql
# get prompt
# get RAG data

# send to Claude or OpenAI or Open  source llms

# based on response -> reply or call tools or run pipeline sor work flows



