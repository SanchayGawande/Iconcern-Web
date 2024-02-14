from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)
MAX_CONTEXT_QUESTIONS =10

@app.route('/call-gpt')
def callgpt_completions(prompt):
    url = "https://documentcodesk.openai.azure.com/openai/deployments/Codesk/completions?api-version=2022-12-01"
    payload = json.dumps({
    "prompt": prompt,
    "max_tokens": 1000,
    "temperature": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "top_p": 0.5,
    "stop": None
    })
    headers = {
    'Content-Type': 'application/json',
    'api-key': ''
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    print(response)
    return response.get('choices',[{},])[0].get('text','')

@app.route('/call-gpt-chat')
def  callgpt_chat(chat_history):
    url = "https://documentcodesk.openai.azure.com/openai/deployments/Codesk/chat/completions?api-version=2023-03-15-preview"
    messages = [
        { "role": "system", "content":"Assistant is a code generator that writes code using html css without description"} #"You are an AI assistant that writes code using html css with out description" },
    ]
    # messages.append({ "role": "user", "content": prompt })
    messages.append(chat_history)
    print("MESSAGES",messages)
    payload = json.dumps({
    "messages": chat_history,
    "max_tokens": 1000,
    "temperature": 0.7,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "top_p": 0.95,
    "stop": None
    })
    headers = {
    'Content-Type': 'application/json',
    'api-key': ''#insert api key
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()

    return response.get('choices',[{},])[0].get('message',{}).get('content','')



@app.route('/call-gpt-chat-v2')
def  callgpt_chat_v2(prompt,previous_questions_and_answers):
    url = "https://documentcodesk.openai.azure.com/openai/deployments/Codesk/chat/completions?api-version=2023-03-15-preview"
    messages = [
        { "role": "system", "content": "You are an AI assistant that writes code." },
    ]
    # add the previous questions and answers

    print("PREVIOUS QUESTIONS",previous_questions_and_answers['user_input'].items())
    for question, answer in previous_questions_and_answers['user_input'].items():
        messages.append({ "role": "user", "content": question })
        if answer:
            messages.append({ "role": "assistant", "content": answer })
    # add the new question
    print("MESSAGES",messages)
    messages.append({ "role": "user", "content": prompt })
    payload = json.dumps({
    "messages": messages,
    "max_tokens": 1000,
    "temperature": 0.7,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "top_p": 0.95,
    "stop": None
    })
    headers = {
    'Content-Type': 'application/json',
    'api-key': ''
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    print(response)
    return response.get('choices',[{},])[0].get('message',{}).get('content','')


@app.route('/save')
def save():
    return 'Contact Us'

@app.route('/')
def hello_world():
    prompt="write me a html code for a modern book reader form where on click of submit button it should hit a post API and Only respond with code as plain text  and do not explain the code with any words"
    return '''{}'''.format(callgpt_chat(prompt))


if __name__ == '__main__':
    app.run(debug=True)
