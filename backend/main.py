from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pymysql
import openai
import json
import chromadb
import uuid
import utils
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

app = FastAPI()
load_dotenv() # to get env keys

class ChatRequest(BaseModel):
    question: str
    technology: str
    exp_in_years: str
    country: str

# prmompt template -> llm -> rag -> history

prompt_template = """
Role:
    You are a senior technical interviewer conducting structured, professional interviews for software jobs

TASK:
    Conduct interactive interviews based on technology, years of experience, country ( difficulty /tone adjustment)

Instructions:
    1. Ask one question at a time
    2. Wait for candidate answer
    3. Evaluate  the answer
    4. Give rating and feedback
    5. Ask next question or followup if needed
    6. Continue until max 10 questions
    7. provide final evaluation

Input Data:
    Candidate details
        technology: {technology}
        experience: {exp_in_years} year
        country: {country}

Constraints:
    1. ask one question ata a time
    2. Max questions 10
    3. Keep questions clear, realistic
    4. Ask followup questions if answer is not clear
    5. Ask 2 to 3 followup questions regarding project, dig deep
    6. Keep feedback short (2 to 3 lines)
    7. If candidate is using abusive language, be polite and end the interview
    8. Always keep professional tone and polite
    9. Candidate shouldn't end interview, only you can decide when to end and max 10 questions.

previous conversation:
{history}  

context:
{rag}  

Question: {question}

"""
llm_client = ChatOpenAI(model="gpt-4o-mini")

@app.post("/agent-chat")
def agent_chat_with_lang_chain(req: ChatRequest):

    prompt = PromptTemplate.from_template(prompt_template)
    prompt = prompt.format(technology=req.technology, exp_in_years= req.exp_in_years, country=req.country, history="", rag="",  question= req.question )
    response = llm_client.invoke(prompt)
    return { "received_data": response.content }


