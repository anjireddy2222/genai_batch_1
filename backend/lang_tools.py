
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

llm_client = ChatOpenAI(model="gpt-5.5")

internet_search_tool = DuckDuckGoSearchRun()

results = internet_search_tool.run("openai ipo")

prompt = f"""
summarize and give me data in bullet points.

data
{results}
"""

llm_results = llm_client.invoke(prompt)

print( llm_results.content )










