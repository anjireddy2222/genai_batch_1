
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pymysql
import openai
import json
import chromadb
import uuid
import utils


app = FastAPI()

# run fastapi project:  uvicorn app:app --reload  

# app -> file name -> app.py
# app: fastapi object

# receive data -> connect with ai -> work flow -> return response

# create api -> for every task

# method -> api path -> data

# connection open, execute, connection close

def get_db_connection():
    connection = pymysql.connect(host="localhost", user="root", port=3306, password="123456789", database="amazon_db", cursorclass=pymysql.cursors.DictCursor)
    return connection



@app.get("/")
def index():
    print("server running")
    return { "result": "success", "data": {}, "message": "Server running" }


@app.get("/get-llms") # api path
def get_llms():
    return { "result": "success", "message": "ok", "data": ["claude", "openai"]}

# courses, expereince, country

# name, email, password

class Signup(BaseModel):
    name: str
    email: str
    password: str

@app.post("/signup")
def signup(signup: Signup):
    # get data
    print(signup.name, signup.email, signup.password)
    # prepare query
    query = "insert into users(`name`, `email`, `pword`) values (%s, %s, %s)"
    # establish connection
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(query, (signup.name, signup.email, signup.password ))

    connection.commit()
    connection.close()

    return { "result": "success", "message": "account created succesfully", "data": signup }
    # insert into users(`name`, `email`, `pword`) values ('Bhavitya', 'contact@bhavitya.ai', '12345678' ); 


@app.get("/users")
def get_users():
    # connect -> run select query -> return data
    query = "select user_id, name, email, pword from users"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(query)

    users = cursor.fetchall()
    conn.close()

    return { "result": "success", "message": "users data", "data": users }

class ChatData(BaseModel):
    business_id: str
    user_id: str
    message: str


@app.post("/api/wa/chat")
def ai_chat(chat_data: ChatData):
    
    query = "select * from conversations where user_id=%s and business_id =%s "
    conn = get_db_connection();
    cursor = conn.cursor()

    cursor.execute(query, (chat_data.user_id, chat_data.business_id))

    history =cursor.fetchall()

    conn.close()

    print( chat_data.business_id)
    return { "result": "success", 'message': "our team will get back to you", "data": history }


# get conversation history -> mysql
# get prompt
# get RAG data

# send to Claude or OpenAI or Open  source llms

# based on response -> reply or call tools or run pipeline sor work flows


# openai package -> api key -> 

openai_api_key = ""
# question and answer
# chat

openai_client = openai.OpenAI(api_key=openai_api_key)

class AskData(BaseModel):
    question: str


@app.post('/ask')
def openai_ask(req: AskData):

    ai_response = openai_client.responses.create( model=llm_model, input=req.question )
    print(ai_response)
    return{ "response": ai_response }


@app.post('/ask-json')
def openai_ask_json_output(req: AskData):
    prompt = f""" 
        Question:  { req.question }
        Do not return json inside markdown or code block
        JSON format
        {{
            "short_answer": "",
            "key_points": [ ],
            'example": ""
        }}
    """
    ai_response = openai_client.responses.create(model=llm_model, input=prompt)
    json_response = json.loads(ai_response.output_text)
    
    return { "response": json_response }


@app.post("/chat")
def openai_chat(req: AskData):
    print(req)
    messages =[]
    # add prompt, history, latest message
    prompt_msg = {
        "role": "system",
        "content": f""" 
            Do not return json inside markdown or code block
            JSON format
            {{
                "short_answer": "",
                "key_points": [ ],
                'example": ""
            }}
        """
    }
    messages.append(prompt_msg)
    # add history to messages list (array)
    messages.append( {
        "role": "user",
        "content": req.question
    } )

    response = openai_client.chat.completions.create(
        model=llm_model,
        messages=messages
    )
    
    json_response = json.loads(response.choices[0].message.content)

    return { "response": json_response }




@app.post("/enq")
def openai_enq(req: AskData):
    connection = get_db_connection()
    cursor = connection.cursor()
    messages = []
    prompt_msg = {
        "role": "system",
        "content": f""" 
            You are sales assistant for softwareschool. softwareschool is providing coding classes in telugu for job seekers.
            guide, qualify and suggest best courses based on user profile. 
            Courses:
            Name: ReactJS
            technologies: html, css, bootstrap, JS, reactjs
            mode: recorded classes
            demo ink: https://ss.co/react-demo
            syllabus: https://ss.co/react-syllabus

            Name: genAI
            technologies: llm, prompt engineering, genai, ai agents, langchain
            mode: live classes
            demo ink: https://ss.co/genai-demo
            syllabus: https://ss.co/genai-syllabus

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
        """
    }
    messages.append(prompt_msg)
    # history
    query = "select `msg_role`, `msg_content` from chats;"
    cursor.execute(query)
    history = cursor.fetchall()
    for msg in history:
        messages.append({ "role": msg["msg_role"] , "content": msg["msg_content"]  })
    
    # latest user msg
    messages.append({"role": "user", "content": req.question})
    
    print(messages)

    response = openai_client.chat.completions.create(model= llm_model, messages=messages)

    json_response =  json.loads(response.choices[0].message.content)
    

    # insert user msg
    query = "insert into chats(`msg_role`, `msg_content`) values(%s,%s);"

    cursor.execute(query, ("user", req.question  ))

    # insert ai reply
    query = "insert into chats(`msg_role`, `msg_content`) values(%s,%s);"
    cursor.execute(query, ("assistant", json_response["message"] ))

    connection.commit()
    connection.close()

    return { "response": json_response, "messages": messages } 


chroma_client = chromadb.PersistentClient("./chroma_db") # mysql database
chroma_collection = chroma_client.get_or_create_collection(name="courses")



@app.get("/add-embeds")
def chroma_db_add_data():
    courses_data = [
        "Softwareschool genai course is 8 to 10 weeks long",
        "gen ai course covers prompt engineering, RAG, AI agents, Langchain",
        "Reactjs is recorded classes, online",
        "reactjs covers html, css, bootstrap, js, reactjs",
        "springboot is recorded classes and online only",
        "springboot covers java, mysql, springboot, few aws concpets"
    ]
    # id, data, vectors
    response = []
    for data in courses_data:
        vectors = openai_client.embeddings.create(model="text-embedding-3-small", input=data)
        #chroma_collection.add( ids=[ str( uuid.uuid4() ) ], documents=[data], embeddings=[vectors.data[0].embedding] )
        response.append({'data': data, 'vectors': vectors})

    return response


@app.post("/chat-with-embeds")
def chat_with_embeds(req: AskData):
    # reactjs -> vectors -> 
    vectors = openai_client.embeddings.create(model="text-embedding-3-small", input=req.question)
    vectors = vectors.data[0].embedding
    embed_results = chroma_collection.query( query_embeddings=[vectors], n_results=3 )

    return embed_results


@app.post("/rag-upload-file")
def rag_file_uploader(file: UploadFile = File(...) ):
    # print("RAG: file upload")
    file_name = file.filename.lower()
    text = ""

    if file_name.endswith(".pdf"):
        print("pdf")
        text = utils.read_pdf(file)
    
    if file_name.endswith(".docx"):
        print("document")
        text = utils.read_docs(file)

    if file_name.endswith(".txt"):
        print("text file")
        text = utils.read_txt_file(file)

    # print(text)
    chunks = utils.create_chunks(text)
    print(chunks)



    return { "response": text }





