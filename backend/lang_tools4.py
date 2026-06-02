from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
import json
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
# sql db details
# convert user input to sql query -> 
# run that query using tool
# get ai summary for that sql data
app = FastAPI()
load_dotenv()

llm_client = ChatOpenAI(model="gpt-5.5")
db = SQLDatabase.from_uri("mysql+pymysql://root:123456789@localhost:3306/amazon_db")
# "mysql+pymysql://user_name:password@server url:port number/db name"

db_tool = QuerySQLDataBaseTool(db=db)

class UserInput(BaseModel):
    user_input: str

@app.post("/db-chat")
def db_chat(req: UserInput):
    user_input = req.user_input

    sql_prompt = f"""
    you are a SQL expert.

    Convert user question into SQL query

    Tables:

    Name: users
    Columns: user_id, name, email, pword, created_on

    Name: interviews
    Columns: interview_id, user_id, int_status (values: progress, completed, invitation pending: waiting for candidate acceptance ), int_started_at, int_ended_at, result

    User question: {user_input}

    Always return response in JSON format. don't put json inside quotes or code block
    {{
    "sql_query": "generated sql query"
    }}
    """

    sql_response = llm_client.invoke(sql_prompt)
    # print(sql_response)
    sql_response = json.loads(sql_response.content)
    # print(sql_response)
    sql_query = sql_response['sql_query']
    print(sql_query)

    db_results = db_tool.run(sql_query)
    print(db_results)

    summary_prompt = f"""
    user question: {user_input}
    database result: {db_results}
    generate helpful summary.

    Always return data in JSOn format. don't put JSOn data inside code/json block or quotes
    {{
    "ai_response":"summary"
    }}
    """

    final_response = llm_client.invoke(summary_prompt)
    final_response = json.loads(final_response.content)

    final_response  = final_response['ai_response']

    return { "user_enquiry": user_input, "result": final_response }





