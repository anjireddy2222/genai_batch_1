
from dotenv import load_dotenv
from fastapi import FastAPI

from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_agent
from langchain.tools import tool
from pydantic import BaseModel
import middleware as md
from langchain.agents.middleware import ToolRetryMiddleware, ModelRetryMiddleware, ModelCallLimitMiddleware, ToolCallLimitMiddleware, ModelFallbackMiddleware

load_dotenv()

app = FastAPI()

search_tool = DuckDuckGoSearchRun()

@tool()
def reactjs_demo_tool():
    """use this tool to get reactjs demo link"""
    raise Exception("ReactJS demo tool is down. Please retry after sometime")
    return """Reactjs demo link https://yt.com/reactjs"""

@tool( description="use this tool to get java springboot demo link")
def spring_demo_tool():
    return """Java springboot demo link https://yt.com/spring"""


@tool( description="use this tool to get genai demo link")
def genai_demo_tool():
    return """genai demo link https://yt.com/genai"""

@tool( description= "use this tool to get course name from ids")
def course_name(course_id: str):
    if course_id == "1":
        return "ReactJS"
    if course_id == "2":
        return "GenAI"
    if course_id == "3":
        return "Java"
    
    return "I don't know"





tools = [ search_tool, reactjs_demo_tool, spring_demo_tool, genai_demo_tool, course_name ]

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

agent = create_agent("openai:gpt-10", 
                     tools=tools, 
                     system_prompt=prompt, 
                     response_format=AiResponse, 
                     name="ss_sales_agent",
                     middleware=[ 
                         md.LoggingMiddleware(), 
                         ModelRetryMiddleware(max_retries=3, max_delay=10 ),
                         ToolRetryMiddleware(max_retries=2, max_delay=3),
                         ModelCallLimitMiddleware(run_limit=100, exit_behavior="error"),
                         ToolCallLimitMiddleware(run_limit=20, tool_name="course_name",exit_behavior="error"),
                         ModelFallbackMiddleware("openai:gpt-5.5")
                     ]
                    )


@app.get("/")
def index(req: UserInput):
    try:

        input_data = {
            "messages": [
                { "role": "user","content": req.msg }
            ]
        }

        response = agent.invoke( input_data )
        
        # whatsapp send api : from: 919032029072, to: 918019032313, text: ai_reply, oauth token
        return { "data": response }
    except Exception as e:
        return e





