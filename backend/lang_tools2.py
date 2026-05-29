
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import RequestsGetTool
# headers, cookies, 
from langchain_community.utilities.requests import TextRequestsWrapper

load_dotenv()

llm_client = ChatOpenAI(model="gpt-5.5")

api_wrapper = TextRequestsWrapper()

api_tool = RequestsGetTool( requests_wrapper=api_wrapper, allow_dangerous_requests=True )

result = api_tool.run("https://dummyjson.com/products")

# print( result )

prompt = f"""
i want products with stock greater than 10. filter and give me data in JSOn format only. just return product id, title and stock.

data:
{result}

"""


result = llm_client.invoke(prompt)

print( result.content )

