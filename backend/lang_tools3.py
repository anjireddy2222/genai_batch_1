from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import RequestsPostTool
# headers, cookies, 
from langchain_community.utilities.requests import TextRequestsWrapper
import json

load_dotenv()

llm_client = ChatOpenAI(model="gpt-5.5")

headers= {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer lgkghglaglakghag'
    }

api_wrapper = TextRequestsWrapper( headers=headers )

api_tool = RequestsPostTool( requests_wrapper= api_wrapper, allow_dangerous_requests =True)

post_data = json.dumps({
    "url": "https://dummyjson.com/products/add",
    "data": {
        "title": 'BMW Pencil'
    }
})

result = api_tool.run(post_data)

print( result )


