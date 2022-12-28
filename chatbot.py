import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')
completion = openai.Completion()

start_chat_log = '''Human: Hello, who are you?
AI: Hello, I am Juno, your virtual assistant.
'''

def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    response = completion.create(
        prompt=prompt, engine="text-davinci-002", stop=['\nHuman'], temperature=0.5,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=150)
    answer = response.choices[0].text.strip()
    return answer

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}Human: {question}\nAI: {answer}\n'
chat_log=None
question='What is  bitcoin?'
answer= (ask(question))
chat_log=append_interaction_to_chat_log(question,answer, chat_log)

question = 'Buy me 10 bitcoins'
answer=ask(question)
chat_log=append_interaction_to_chat_log(question,answer, chat_log)

print(chat_log)




