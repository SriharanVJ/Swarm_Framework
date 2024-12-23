import requests
from swarm import Swarm, Agent
from openai import OpenAI

# Initialize the OpenAI client
ollama_client = OpenAI(
    base_url="http://35.244.13.63:11434/v1",
    api_key="ollama"
)

# Initialize the Swarm client
client = Swarm(client=ollama_client)

# Shared context to store user details and flow state
context = {
    "user_details": {},
    "selected_problem": None,
    "selected_doctor": None,
    "selected_time_slot": None
}

# Define function to collect user details
def get_user_details():
    global context
    if not context["user_details"]:
        return {
            "status": "pending",
            "message": (
                "Please provide the following details:\n"
                "1. Name\n"
                "2. Age\n"
                "3. Email\n"
                "4. Phone Number\n"
            )
        }
    return {"status": "success", "details": context["user_details"]}

# Function to save collected details
def save_user_details(name, age, email, phone_number):
    global context
    context["user_details"] = {
        "name": name,
        "age": age,
        "email": email,
        "phone_number": phone_number
    }
    return {"status": "success", "message": "User details saved successfully."}

# Define function to display problem list
def choose_problem():
    return {
        "status": "success",
        "problems": ["Fever", "Cold", "Cough", "Head Ache", "Stomach Ache"]
    }

# Define function to save selected problem
def save_problem(problem):
    global context
    context["selected_problem"] = problem
    return {"status": "success", "message": f"Problem '{problem}' saved."}

# Define function to display doctors list
def choose_doctor():
    doctors = {
        "Fever": ["Dr. Smith", "Dr. Johnson"],
        "Cold": ["Dr. Sam", "Dr. Tom"],
        "Cough": ["Dr. Harry", "Dr. Peter"],
        "Head Ache": ["Dr. James", "Dr. David"],
        "Stomach Ache": ["Dr. Robert", "Dr. William"]
    }
    problem = context.get("selected_problem")
    if problem:
        return {"status": "success", "doctors": doctors.get(problem, [])}
    return {"status": "failure", "message": "No problem selected yet."}

# Define function to save selected doctor
def save_doctor(doctor):
    global context
    context["selected_doctor"] = doctor
    return {"status": "success", "message": f"Doctor '{doctor}' saved."}

# Define function to display time slots
def choose_time_slot():
    return {
        "status": "success",
        "time_slots": [
            "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
            "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"
        ]
    }

# Define function to save selected time slot
def save_time_slot(time_slot):
    global context
    context["selected_time_slot"] = time_slot
    return {"status": "success", "message": f"Time slot '{time_slot}' saved."}

# Define function to confirm appointment
def confirm_appointment():
    global context
    if all(context.values()):
        return {
            "status": "success",
            "message": (
                "Appointment confirmed successfully with the following details:\n"
                f"Name: {context['user_details']['name']}\n"
                f"Age: {context['user_details']['age']}\n"
                f"Email: {context['user_details']['email']}\n"
                f"Phone: {context['user_details']['phone_number']}\n"
                f"Problem: {context['selected_problem']}\n"
                f"Doctor: {context['selected_doctor']}\n"
                f"Time Slot: {context['selected_time_slot']}\n"
            )
        }
    return {"status": "failure", "message": "Incomplete details for appointment confirmation."}

# Agent definitions
collect_details_agent = Agent(
    model='llama3.1:latest',
    name='Collect Details Assistant',
    instructions='Collect user details like name, age, email, and phone number.',
    functions=[save_user_details, get_user_details],
    parallel_tool_calls=True
)

problem_display_agent = Agent(
    model='llama3.1:latest',
    name='Problem Display Assistant',
    instructions='Display the problem list to the user and save their selection.',
    functions=[choose_problem, save_problem],
    parallel_tool_calls=True
)

doctor_display_agent = Agent(
    model='llama3.1:latest',
    name='Doctor Display Assistant',
    instructions='Display the doctor list based on the selected problem and save their choice.',
    functions=[choose_doctor, save_doctor],
    parallel_tool_calls=True
)

doctor_appointment_agent = Agent(
    model='llama3.1:latest',
    name='Doctor Appointment Assistant',
    instructions='Display time slots, save the user selection, and confirm the appointment.',
    functions=[choose_time_slot, save_time_slot, confirm_appointment],
    parallel_tool_calls=True,
    input_type=Agent
)

manager_agent = Agent(
    model='llama3.1:latest',
    name='Manager Assistant',
    instructions='Direct users to the appropriate assistant based on their current progress.',
    functions=[
        collect_details_agent,
        problem_display_agent,
        doctor_display_agent,
        doctor_appointment_agent
    ]
)

# Task description for the manager
task = (
    "You are a doctor appointment booking assistant. Guide the user through these steps:\n"
    "1. Collect user details like name, age, email, and phone number.\n"
    "2. Display the problem list to the user.\n"
    "3. Display the doctor list based on the selected problem.\n"
    "4. Schedule an appointment by showing available time slots.\n"
    "5. Confirm the appointment with all details."
)

# Main execution
if __name__ == "__main__":
    print("Welcome to the user details collection system")
    while True:
        user_prompt = input("> ")
        if user_prompt.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        try:
            response = client.run(
                agent=manager_agent,
                messages=[
                    {"role": "system", "content": task},
                    {"role": "user", "content": user_prompt}
                ]
            )
            print(response.messages[-1]['content'])
        except Exception as e:
            print(f"Error: {e}")
