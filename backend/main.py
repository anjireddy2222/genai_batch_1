from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pymysql
import openai
import json
import chromadb
import uuid
import utils
from dotenv import load_dotenv
import templates
import os
import tools

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

app = FastAPI()
load_dotenv() # to get env keys

class ChatRequest(BaseModel):
    question: str
    technology: str
    exp_in_years: str
    country: str
    interview_id: str
    user_id: str

# prmompt template -> llm -> rag -> history

"""

user_id, user answer, ai question

chats table
chat_id  (auto increment), interview_id ,  user_id, data, user_type ( user, assistant)


interviews
interview_id, user_id, status ( progress, completed), started_at, completed_at, result

"""

def get_db_connection():
    connection = pymysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), port=int(os.getenv("DB_PORT")), password=os.getenv("DB_PASSWORD"), database=os.getenv("DB_NAME"), cursorclass=pymysql.cursors.DictCursor)
    return connection


llm_client = ChatOpenAI(model="gpt-5.5")

@app.post("/agent-chat")
def agent_chat_with_lang_chain(req: ChatRequest):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "select `data`, `user_type` from interview_data where interview_id=%s;"
    cursor.execute(query, (req.interview_id))
    history = cursor.fetchall()
    history_data = ""
    for data in history:
        history_data = f" {history_data} \n {data['user_type']}:{data['data']} "

    prompt = templates.interview_prompt.format(technology=req.technology, exp_in_years= req.exp_in_years, country=req.country, history=history_data, rag="",  question= req.question )
    print("## prompt ##")
    print(prompt)
    response = llm_client.invoke(prompt)

    response = json.loads(response.content)

    # insert user msg
    query = "insert into interview_data(`interview_id`, `user_id`, `data`, `user_type`) values(%s,%s, %s, %s);"

    cursor.execute(query, (req.interview_id, req.user_id,  req.question, "user"  ))

    # insert ai reply
    query = "insert into interview_data(`interview_id`, `user_id`, `data`, `user_type`) values(%s,%s, %s, %s);"
    cursor.execute(query, (req.interview_id, req.user_id, response["reply"], "assistant" ))

    connection.commit()
    connection.close()

    if response["is_interview_completed"]:
        print("interview completed")
        tools.send_email("contact@ss.co", "Interview status", "Hi Anji,\n Please find the below details. \n ha gahkhas gahsg saskgagahaslga\n Thank you")



    return { "received_data": response}


