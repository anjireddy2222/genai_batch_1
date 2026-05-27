from langchain.tools import tool

@tool
def send_email(subject: str, body: str, to_email: str):
    """
    use this tool to send email to hr when interview is completed
    """
    print("#######")
    # print("To: " + to + "\n")
    print("sub: " + subject + "\n")
    print("body: " + body + "\n")
    print("email sent")

@tool(description="use this tool to provide access to HR portal once company email is assigned")
def provide_access():
    print("access tool")


@tool(description="use this tool to add new lead in zoho crm")
def add_new_lead_zoho():
    print("create new zoho lead")




