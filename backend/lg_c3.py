from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import TypedDict

load_dotenv()

llm_client = ChatOpenAI(model="gpt-5.5")

class ChatState(TypedDict):
    message: str

def chat_node(state):
    print("llm")
    response = llm_client.invoke(input="hi")
    state["message"] = response.content
    return state

graph_builder = StateGraph(ChatState)

graph_builder.add_node("chat_node", chat_node)

graph_builder.add_edge(START, "chat_node")
graph_builder.add_edge("chat_node", END)

workflow = graph_builder.compile()

result = workflow.invoke({"message": ""})

print( result )

