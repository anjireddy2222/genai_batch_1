from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
load_dotenv() # to get env keys

llm_client = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, top_p=1)
# response = llm_client.invoke("explain RAG")

# print( response.content )

# llm -> prompt -> history -> RAG -> tools 
# prompt -> role -> instructions -> rules -> history -> RAG -> question
rag = """
Course 1:
Name: ReactJS
syllabus: react syllabus link  test
demo: react demo link test
technologies: html, css, bootstrap, js, reactjs

Course 2:
Name: Java springboot
syllabus: spring syllabus link  test
demo: spring  demo link test
technologies: html, css, bootstrap, js, reactjs

"""

history = """
user: hi
assistant: welcome to softwareschool
"""

question = "do you have nodejs?"

prompt_template = """
You are sales assistant for softwareschool. softwareschool is providing coding classes in telugu for job seekers.
guide, qualify and suggest best courses based on user profile. 
Courses:


if they are asking to talk to someone, we are available form 10 am IST to 6PM IST on whatsapp 9032029072 and email: contact@softwareschool.co and 
check if they have any preferred time slot for the call so that our team can call them

previous conversation:
{history}

context:
{rag}

question: {question}
"""
print(prompt_template)

prompt = PromptTemplate.from_template(prompt_template)
prompt = prompt.format(history=history, rag=rag, question=question  )

print(prompt)

response = llm_client.invoke(prompt)

print("######")

print( response.content )

# install packages -> import -> create llm client object -> pass prompt or question to llm client


