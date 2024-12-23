import requests
from swarm import Swarm, Agent
from openai import OpenAI






ollama_client=OpenAI(
    base_url="http://35.244.13.63:11434/v1",
    api_key="ollama"
)

client=Swarm(client=ollama_client)

user_details={}


def get_user_details(name=None, age=None, email=None, phone_number=None):
    """You need to collect the user details

    Args:
        ask to the user to provide the name (str),
        ask to the user to provide the age (int),
        ask to the user to provide the email (str),
        ask to the user to provide the phone number (str)

    Returns:
        stored in the user_details dictionary
    """
    
    params = {
        "name": name,
        "age": age,
        "email": email,
        "phone_number": phone_number
    }
    print("x-x-x-x-x-x-x-x-x-x please tell your details step by step")
    
    response = {"status": "success", "details": params}
    return response





def choose_problem():
    print("x-x-x-x-x-x-x-x-x-x problem")
    problems_list=["Fever","Cold","Cough","Head Ache","Stomach Ache"]
    
    response=requests.get(params=problems_list)
    return response

def choose_doctor():
    print("x-x-x-x-x-x-x-x-x-x doctor")
    doctors={
        "Fever":["Dr. Smith","Dr. Johnson"],
        "Cold":["Dr.Sam","Dr. Tom"],
        "Cough":["Dr. Harry","Dr. Peter"],
        "Head Ache":["Dr. James","Dr. David"],
        "Stomach Ache":["Dr. Robert","Dr. William"]
        
    }
    response=requests.get(params=doctors)
    return response

def choose_time_slot():
    print("x-x-x-x-x-x-x-x-x-x time slot")
    time_slots=["9:00 AM","10:00 AM","11:00 AM","12:00 PM","1:00 PM","2:00 PM","3:00 PM","4:00 PM","5:00 PM"]
    response=requests.get(params=time_slots)
    return response

def confirm_appointment():
    print("x-x-x-x-x-x-x-x-x-x confirm appointment")
    response=requests.get(params="confirm appointment")
    return response

def transfer_to_collect_details_assistant():
    print("x-x-x-x-x-x-x-x-x-x Collecting the user details")
    return collect_details_agent


def transfer_to_problem_display_assistant():
    print("x-x-x-x-x-x-x-x-x-x Displaying the problem")
    return problem_display_agent


def transfer_to_doctor_display_assistant():
    print("x-x-x-x-x-x-x-x-x-x Displaying the doctor details")
    return doctor_display_agent

def transfer_to_doctor_appointment_assistant():
    print("x-x-x-x-x-x-x-x-x-x Scheduling the appointment")
    return doctor_appointment_agent





collect_details_agent=Agent(
    model='llama3.1:latest',
    name='collect_details Assistant',
    instructions='When the user said i need to book an appoinment you need to collect the user details like name,age,email,phone number',
    functions=[get_user_details]
)

problem_display_agent=Agent(
    model='llama3.1:latest',
    name='problem_display Assistant',
    instructions='When the user details are collected successfully, You need to display the problem to the user which is in the list in choose_problem function',
    functions=[choose_problem]
)

doctor_display_agent=Agent(
    model='llama3.1:latest',
    name='doctor_display Assistant',
    instructions='When the user details and problem are collected successfully, You need to display the doctor list to the user which is in the list in choose_doctor function',
    functions=[choose_doctor]
)

doctor_appointment_agent=Agent(
    model='llama3.1:latest',
    name='doctor_appointment Assistant',
    instructions='When the user details,problem and doctor are collected successfully, You need to schedule the appointment with the doctor and display the time slot to the user which is in the list in choose_time_slot function',
    functions=[confirm_appointment]
)

manager_agent=Agent(
    model='llama3.1:latest',
    name='Manager Assistant',
    instructions='You help users by directing them to the right assistant.',
    functions=[transfer_to_collect_details_assistant,transfer_to_problem_display_assistant,
               transfer_to_doctor_display_assistant,transfer_to_doctor_appointment_assistant],
    
)

task="""
You are a doctor appointment booking assistant.Ask to the user step by step below questions and get the prompt.
First you need to collect the user details like name,age,email,phone number.
Then you need to display the problem list to the user which we have mentioned.
Then you need to display the doctor list to the user which we have mentioned.
Then you need to schedule the appointment with the doctor.
Then you need to confirm the appointment with the user with showing the collected details.
"""

if __name__=="__main__":
    print("Welcome to the user details collection system")
    while True:
        user_prompt=input("> ")
        if user_prompt.lower() in ["exit","quit","bye"]:
            break
        try:
            response=client.run(
            agent=manager_agent,
            messages=[
                {"role": "user", "content": task},
                {"role": "user", "content": user_prompt}
            ]
    )
        
            print(response.messages[-1]['content'])
            
        except Exception as e:
            print(e)