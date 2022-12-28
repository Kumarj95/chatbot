from flask import Flask, request,session
from twilio.twiml.messaging_response import MessagingResponse
app = Flask(__name__)
from chatbot import ask,append_interaction_to_chat_log
app.config['SECRET_KEY'] = 'top-secret!'


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values['Body']

    chat_log=None
    question=incoming_msg
    chat_log = session.get('chat_log')
    answer=ask(question,chat_log)
    session['chat_log']=append_interaction_to_chat_log(question,answer,chat_log)

    # use the incoming message to generate the response here

    r = MessagingResponse()
    r.message(answer)
    return str(r)


if __name__ == '__main__':
    app.run()
