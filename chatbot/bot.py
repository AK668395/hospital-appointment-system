import random

def get_bot_response(message):

    message = message.lower()

    greetings = [
        "Hello! How can I assist you today?",
        "Hi there! Welcome to CityCare Hospital.",
        "Greetings! How may I help you?"
    ]

    doctor_responses = [
        "Our doctors are available Monday to Saturday from 9 AM to 7 PM.",
        "Specialist doctors are available based on appointment schedule."
    ]

    appointment_responses = [
        "You can easily book an appointment from the appointment page.",
        "Please provide patient details on the booking page to confirm appointment."
    ]

    thanks_responses = [
        "You're welcome!",
        "Happy to help!",
        "Glad I could assist you."
    ]

    if "hello" in message or "hi" in message:
        return random.choice(greetings)

    elif "doctor" in message:
        return random.choice(doctor_responses)

    elif "appointment" in message or "book" in message:
        return random.choice(appointment_responses)

    elif "timing" in message or "open" in message:
        return "CityCare Hospital is open daily from 9 AM to 8 PM."

    elif "emergency" in message:
        return "For emergencies, please dial 108 immediately."

    elif "thank" in message:
        return random.choice(thanks_responses)

    elif "name" in message:
        return "I am your AI Hospital Assistant."

    elif "where" in message:
        return "Our hospital is located in Bangalore."

    elif "fees" in message:
        return "Consultation fees depend on the doctor and department."

    elif "bye" in message:
        return "Take care! Stay healthy."

    else:
        return f"I understand you said: '{message}'. Could you please explain a little more?"