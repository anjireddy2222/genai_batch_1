# state
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class PasswordResetState(TypedDict):
    email: str
    is_email_exists: bool
    is_reset_link_sent: bool
    status: bool
    message: str

class CustomerSupportState(TypedDict):
    email: str
    mobile: str
    order_id: int
    enquiry: str # return, delivery status, refund status, feedback
    ticket_id: int
    ticket_status: bool
    ticket_data: str
    comments: str

# node

def collect_email(state):
    print(f"inside collect_email node: {state}")
    state["email"] = "contact@softwareschool.co"
    return state
    
def check_email(state):
    print(f"inside check_email node: {state}")
    state["is_email_exists"] = True
    return state
   
def send_reset_link_email(state):
    print(f"inside send_reset_link_email node: {state}")
    state["is_reset_link_sent"] = True
    return state
   
def show_result(state):
    print(f"inside show_result node: {state}")
    if state["is_reset_link_sent"] == True:
        state["status"] = True
        state["message"] = "Password reset link sent to your email, please check it. Thank you"
    else:
        state["status"] = False
        state["message"] = "Account doesn't exists with the email you provided"
    return state

# set state/data type
graph_builder = StateGraph(PasswordResetState)
# add nodes
graph_builder.add_node("send_reset_link_email", send_reset_link_email)
graph_builder.add_node("check_email", check_email)
graph_builder.add_node("show_result", show_result)
graph_builder.add_node("collect_email", collect_email)
# connect nodes (add edges) -> define sequence
graph_builder.add_edge(START, "collect_email")
graph_builder.add_edge("collect_email", "check_email")
graph_builder.add_edge("check_email", "send_reset_link_email")
graph_builder.add_edge("send_reset_link_email", "show_result")
graph_builder.add_edge("show_result", END)

agent = graph_builder.compile()

result = agent.invoke({"email": "", "is_email_exists": None, "is_reset_link_sent": None, "status": None})

print("### RESULT ###")
print(result)






