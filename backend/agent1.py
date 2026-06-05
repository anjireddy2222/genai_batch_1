
from dotenv import load_dotenv
from fastapi import FastAPI

from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_agent
from langchain.tools import tool
from pydantic import BaseModel


load_dotenv()

app = FastAPI()

search_tool = DuckDuckGoSearchRun()

@tool()
def reactjs_demo_tool():
    """use this tool to get reactjs demo link"""
    return """Reactjs demo link https://yt.com/reactjs"""

@tool( description="use this tool to get java springboot demo link")
def spring_demo_tool():
    return """Java springboot demo link https://yt.com/spring"""


@tool( description="use this tool to get genai demo link")
def genai_demo_tool():
    return """genai demo link https://yt.com/genai"""


tools = [ search_tool, reactjs_demo_tool, spring_demo_tool, genai_demo_tool ]

prompt = """
you are helpful sales agent for softwareschool. people will message you to enquire about our courses, syllabus and demos. Please be friendly and
ask about their background and just best suitable course.

ReactJS course:
technologies: html, css, bootstrap
mode: recorded

Springboot course:
technologies: java, springboot, mysql
mode: recorded


genai course:
technologies: python, langchain, agents, llm
mode: live

"""

class UserInput(BaseModel):
    msg: str

class AiResponse(BaseModel):
    interested_course: str
    ai_reply: str
    confidence: float

agent = create_agent("openai:gpt-5.5", tools=tools, system_prompt=prompt, response_format=AiResponse, name="ss_sales_agent")


@app.get("/")
def index(req: UserInput):
    input_data = {
        "messages": [
            { "role": "user","content": req.msg }
        ]
    }
    response = agent.invoke( input_data )
    
    # whatsapp send api : from: 919032029072, to: 918019032313, text: ai_reply, oauth token
    return { "data": response }





