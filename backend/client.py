
from fastapi import FastAPI
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


app = FastAPI()


@app.post("/mcp-chat")
async def mcp_chat():
    print("mcp chat")
    # connect to server
    # establish session
    # use session to run operations -> tools list, tools execution
    tools = []
    result = ""
    async with streamable_http_client("http://localhost:8001/mcp") as (read, write, _):
        print("mcp connection")
        async with ClientSession(read, write) as session:
            print("session")
            await session.initialize()
            tools = await session.list_tools()

            result =await session.call_tool("get_courses", arguments={})



             

    return { "data": "mcp chat", "tools": tools, "result": result }


