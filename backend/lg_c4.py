from langgraph.graph import StateGraph, MessagesState, START, END
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from fastapi import FastAPI
load_dotenv()
app = FastAPI()
llm_client = ChatOpenAI(model="gpt-5.5")

chat_agent = create_agent( model=llm_client, tools=[], system_prompt="you are sales agent for softwareschool, we are providing coding classes in telugu, qualify customers, understand their background and suggest best courses" )


def chat_node(state):
    print("agent running inside chat_node")
    response = chat_agent.invoke({ "messages": state["messages"] })
    # print(response)
    state["messages"] = response["messages"][-1]
    return state


graph_builder = StateGraph(MessagesState)
graph_builder.add_node('node1', chat_node)
graph_builder.add_edge(START, 'node1')
graph_builder.add_edge('node1', END)

workflow = graph_builder.compile()

@app.get("/")
def index():
    result = workflow.invoke({
        "messages": [
            {"role": "user", "content": "hi"}
        ]
    })
    return { "response":  result}

    # print(result)






