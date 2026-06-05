from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.file_management.write import WriteFileTool
from langchain_community.tools.file_management.read import ReadFileTool
from pydantic import BaseModel
import json

app = FastAPI()
load_dotenv()


llm_client = ChatOpenAI(model="gpt-5.5")
write_tool = WriteFileTool()
read_tool = ReadFileTool()

class UserInput(BaseModel):
    msg: str

@app.post("/write-tool")
def file_tool(req: UserInput):
    # print(req.msg)
    file_prompt = f"""
    extract file name and content from the below user data. always return data in json format, don't put json under code block or quotes
    
    {{
        "file_name": "file name",
        "file_content": "file content",
        "is_file_name_found": "yes or no",
        "is_file_content_found": "yes or no"
    }}
    user data: {req.msg}
    """

    llm_response = llm_client.invoke(file_prompt)
    response = json.loads(llm_response.content)
    tool_result = ""
    if response["is_file_name_found"] == "yes":
        tool_result = write_tool.run({ "file_path": response["file_name"], "text": response["file_content"], "append":  True })

    return { "data": req.msg, "response": response, "tool_result": tool_result }

@app.post("/read-tool")
def file_read_tool(req: UserInput):
    file_prompt = f"""
    find file name from the user data and return response in json format only, don't put json data inside code blocks or quotes.
    {{
        "file_name": "file name",
        "is_file_name_found": " yes or no"
    }}
    user data: {req.msg}
    """
    llm_response = llm_client.invoke(file_prompt)
    response = json.loads(llm_response.content)
    tool_result = ""
    if response["is_file_name_found"] == "yes":
        tool_result = read_tool.run(response["file_name"])


    return { "data": req.msg, "response": response, "tool_result": tool_result }


