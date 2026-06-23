from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

# interview
# node 1 -> generate offer letter
# node 2 -> approval -> waiting -> 
# node 3 -> if approved -> send offer letter -> end
# node 4 -> if rejected -> send rejection email -> end

class CandidateData(TypedDict):
    name: str
    email: str
    approval: str
    message: str

def offer_letter(state):
    print("offer letter generated")
    return state

def approval(state):
    print("email sent to HR for approval/approval note updated in dashboard")
    int = interrupt("HR approval required")
    print(int)
    state["approval"] = int
    return state

def send_offer_letter(state):
    print("Offer letter sent to " + state["email"])
    return state

def send_rejection_email(state):
    print("Rejection email sent to " + state["email"])
    return state

# conditional route
def check_approval_status(state):
    if state["approval"] == "approved":
        return "send_offer_letter"
    else:
        return "send_rejection_email"

graph_builder = StateGraph(CandidateData)

graph_builder.add_node("send_offer_letter",send_offer_letter)
graph_builder.add_node("approval",approval)
graph_builder.add_node("send_rejection_email",send_rejection_email)
graph_builder.add_node("offer_letter",offer_letter)

graph_builder.add_edge(START, "offer_letter")
graph_builder.add_edge("offer_letter", "approval")
graph_builder.add_conditional_edges("approval", check_approval_status, { "send_offer_letter": "send_offer_letter", "send_rejection_email": "send_rejection_email" } )
graph_builder.add_edge("send_offer_letter", END)
graph_builder.add_edge("send_rejection_email", END)

memory = MemorySaver()

work_flow = graph_builder.compile(checkpointer=memory)

print("### 1st run")
result1 = work_flow.invoke({"name": "anji", "email":"con@ss.co", "approval":"", "message":""}, { "configurable": { "thread_id": "cand_1" }})
result2 = work_flow.invoke({"name": "anji 2", "email":"con2@ss.co", "approval":"", "message":""}, { "configurable": { "thread_id": "cand_2" }})
print(result1)
print(result2)
print("### 2nd run")
result1 = work_flow.invoke(Command(resume="reject"), { "configurable": { "thread_id": "cand_1" }})
result2 = work_flow.invoke(Command(resume="approved"), { "configurable": { "thread_id": "cand_2" }})
print(result1)
print(result2)

