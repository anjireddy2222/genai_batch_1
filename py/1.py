

print("my python code")

print("python code updated")

# data types: text (alphabest, special chars, numbers), numbers, true or false

email =  "contact@softwareschool.co"

user_name = 'Anji Reddy'

print( email )

print( user_name )

mobile_price = 9999

# true false 

is_interview_completed = False

is_human_support_required = True


print( mobile_price )

print( is_human_support_required )

print( is_interview_completed )

interview_prompt = """ Role:
    You are a senior technical interviewer conducting structured, professional interviews for software jobs

TASK:
    Conduct interactive interviews based on technology, years of experience, country ( difficulty /tone adjustment)

Instructions:
    1. Ask one question at a time
    2. Wait for candidate answer
    3. Evaluate  the answer
    4. Give rating and feedback
    5. Ask next question or followup if needed
    6. Continue until max 10 questions
    7. provide final evaluation

Input Data:
    Candidate details
        technology: python
        experience: 1 year
        country: india """


print( interview_prompt )

# list

technologies = [ "html", 'css', 'javascript', "reactjs", "git and github", 858, True ]

student_names = ["name 1", 'name 2', "name 3"]


print( technologies )

# position number: 0, 1, 2, 3, 4, 5, 6
print( technologies[0] )

print( technologies[2] )

print( technologies[6] )


print( student_names[0])
print( student_names[1])

student_emails = ["s1@gmail.com", "s2@gmail.com", 's3@gmail.com']

student_mobiles = [123, 41414, 211]

print( student_names[0], student_emails[0], student_mobiles[0])



student = {
    "name": "student 1",
    "mobile": 85454,
    "email": "s1@gmail.com",
    "exp": 4
}


print( student )

print( student["name"] )


print( student["exp"] )


# is_interview_completed : True , False : True
is_interview_completed = True
print(is_interview_completed)

if is_interview_completed == True:
    print("Thanks for attending interview, we will get back to you soon")
    print("dssh")

if is_human_support_required == True:
    print("send email")

# if( ){
#     hashsdhs
#     SystemError
#     sjsj
# }



# loops
# student_mobiles = [123, 41414, 211]
student_mobiles = []
for mobile in student_mobiles:
    print(mobile)


for name in student_names:
    print(name)






