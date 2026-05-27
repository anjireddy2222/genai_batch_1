from mcp.server.fastmcp import FastMCP

mcp_server = FastMCP("GenAI-MCP")


@mcp_server.tool(name="get_courses", description="use it to get available courses from softwareschool")
def get_courses():
    courses_list = ["Reactjs", "Springboot", "GenAI", "NodeJS"]
    return courses_list


@mcp_server.tool(name="password_reset", description="use it to reset users password")
def password_reset(email: str):
    print("checking email in users table")
    print("email found")
    print(f"new password sent to {email}.")

    return "New password sent to user email"


app = mcp_server.streamable_http_app()




