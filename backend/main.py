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

class InterviewResponse(BaseModel):
    reply: str
    is_follow_up: bool
    previous_question_overall_rating: int
    previous_question_technical_rating: int
    previous_question_comm_rating: int
    final_overall_rating: int
    final_technical_rating: int
    final_comm_rating: int
    is_interview_completed: bool

       

llm_client = ChatOpenAI(model="gpt-5.5")
llm_client_for_tools = llm_client.bind_tools([tools.send_email, tools.provide_access, tools.add_new_lead_zoho])

llm_interview_client = ChatOpenAI(model="gpt-5.5")
llm_interview_client = llm_interview_client.with_structured_output(InterviewResponse)

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
    # print("## prompt ##")
    # print(prompt)
    response = llm_interview_client.invoke(prompt)
    # print( response )
    # response = json.loads(response.content)

    # insert user msg
    query = "insert into interview_data(`interview_id`, `user_id`, `data`, `user_type`) values(%s,%s, %s, %s);"

    cursor.execute(query, (req.interview_id, req.user_id,  req.question, "user"  ))

    # insert ai reply
    query = "insert into interview_data(`interview_id`, `user_id`, `data`, `user_type`) values(%s,%s, %s, %s);"
    cursor.execute(query, (req.interview_id, req.user_id, response.reply, "assistant" ))

    connection.commit()
    connection.close()
    tool_response = {}
    if response.is_interview_completed == True :
        # print("interview completed")
        tool_prompt = f"""
            interview is completed. send interview email to HR. 
            candidate ratings:

            Overall rating: {response.final_overall_rating}
            technical rating: {response.final_technical_rating}
            communication rating: {response.final_comm_rating}

            send email to HR: contact@ss.co
        """
        tool_response = llm_client_for_tools.invoke(tool_prompt)
        for tool in tool_response.tool_calls:
            print(tool)
            if tool["name"] == "send_email":
                tools.send_email.invoke(tool["args"])
            if tool["name"] == "provide_access":
                tools.provide_access.invoke(tool["args"])


        # tools.send_email("contact@ss.co", "Interview status", "Hi Anji,\n Please find the below details. \n ha gahkhas gahsg saskgagahaslga\n Thank you")



    return { "received_data": response, "tool_response": tool_response }


