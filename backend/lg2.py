from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class PasswordResetState(TypedDict):
    num: int

def node1(state):
    print(f"inside node1 : {state}")
    state["num"] = state["num"] + 1
    print( state["num"] )
    return state
    
def node2(state):
    print(f"inside node2 : {state}")
    state["num"] = state["num"] + 2
    print( state["num"] )
    return state
   
def node3(state):
    print(f"inside node3 : {state}")
    state["num"] = state["num"] + 3
    print( state["num"] )
    return state


graph_builder = StateGraph(PasswordResetState)
graph_builder.add_node("node1", node1)
graph_builder.add_node("node2", node2)
graph_builder.add_node("node3", node3)

graph_builder.add_edge(START, "node1")
graph_builder.add_edge("node1", "node2")
graph_builder.add_edge("node1", "node3")
graph_builder.add_edge("node3", END)

agent = graph_builder.compile()

result = agent.invoke({"num": 1})

print("### RESULT ###")
print(result)


