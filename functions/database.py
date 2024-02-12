import json
import random

# Get Recent Messages
def get_recent_messages():
    file_name = "stored_data.json"
    learn_instruction = {
        "role": "assistant",
        "content": "You are a customer who just received a call from a stock market broker (me, the user). Approach the conversation with a mix of curiosity, questions, and potential concerns. Ask about the broker's investment strategies, inquire about recent market trends, and express your preferences regarding risk and return. Feel free to provide personal details that are relevant to the conversation. The broker may suggest specific stocks or investment opportunities. Respond authentically as if you are actively engaging with a broker."
    }

    messages = []

    messages.append(learn_instruction)

    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)

    except Exception as e:
        print(e)
        pass
    
    return messages

def store_message(request_message, response_message):
    file_name = "stored_data.json"

    messages = get_recent_messages()[1:]

    user_message = {"role": "user", "content": request_message}
    assitant_message = {"role": "assistant", "content": response_message}
    messages.append(user_message)
    messages.append(assitant_message)

    with open(file_name, 'w') as f:
        json.dump(messages, f)

def reset_messages():
    open("stored_data.json", "w")
