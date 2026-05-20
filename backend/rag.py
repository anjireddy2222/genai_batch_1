
from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# load data/knowledge
documents = SimpleDirectoryReader("data").load_data();
# llm -> openai llm
index = VectorStoreIndex.from_documents(documents); # vectors
# prompt -> 
openai_llm = OpenAI(model="gpt-5.5")

# user query
query_engine = index.as_query_engine(llm=openai_llm)

# llama -> run query -> 

prompt_msg = f""" 
            You are sales assistant for softwareschool. softwareschool is providing coding classes in telugu for job seekers.
            guide, qualify and suggest best courses based on user profile. 
            Courses:
            

            if they are asking to talk to someone, we are available form 10 am IST to 6PM IST on whatsapp 9032029072 and email: contact@softwareschool.co and 
            check if they have any preferred time slot for the call so that our team can call them

            Do not return json inside markdown or code block
            always return data in JSOn format as mentioned below 
            JSON format
            {{
                "course": "interested course based on chat",
                "score":"cold, warm, hot, ready to pay",
                'message": "yur reply",
                "asking_for_call": "true or false based on conversation (if they are asking to talk to someone)",
                "preferred_time_slot": "user's preferred call date and time based on your conversation",
                "mobile_number": "user's mobile number"
            }}

            Previous conversations:
            user: 
            Assistant: 

            user: 
            Assistant:

            user: 
            Assistant:

            Question: do you have springboot
        """
    

response = query_engine.query(prompt_msg)

print( response )

"""
Create API
@app.post("/chat-with-llama)
(req: AskData)

    # get history from db
    # loop and create history string
    # add histroy and user question in prompt

    # run llma query engine

Previous conversations:
            {history_data}

            Question: {req.qustion}

"""

# REST API


"""


Frontend → HTTP Request 

→ Controller → Service 

→ Repository → Database 

→ JSON Response 

→ Frontend UI



"""