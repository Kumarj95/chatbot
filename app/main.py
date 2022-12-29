from flask import Flask, request,session
from twilio.twiml.messaging_response import MessagingResponse
app = Flask(__name__)
from .chatbot import *
import  pymongo
import os
from datetime import datetime, timezone

app.config['SECRET_KEY'] = 'top-secret!'
client = pymongo.MongoClient( os.environ.get('MONGO_URI'))
db = client.db
text_logs= db.text_logs
@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values['Body']
    incoming_phone= request.values['From']
    if('phone_1' not in sorted(list(text_logs.index_information()))):
        text_logs.create_index([('phone', pymongo.ASCENDING)],
                                    unique=True)
    message={"phone":incoming_phone, "Message": {"body":incoming_msg, "time":datetime.now(timezone.utc) }}
    exists = text_logs.find_one({"phone":message["phone"]})
    if not exists:
        text_logs.insert_one({"phone":message["phone"], "messages":[message["Message"]]})
    else:
        newTextLog=exists
        newTextLog["messages"].append(message["Message"])
        text_logs.update_one({"phone":message["phone"]}, {"$set":newTextLog} ,upsert=False)
    
    # if('phone_1' not in sorted(list(text_logs.index_information()))):
    #     text_logs.create_index([('phone', pymongo.ASCENDING)],
    #                                 unique=True)

    chat_log=None
    question=incoming_msg
    chat_log = session.get('chat_log')
    answer=ask(question,chat_log)
    session['chat_log']=append_interaction_to_chat_log(question,answer,chat_log)

    # use the incoming message to generate the response here

    r = MessagingResponse()
    r.message(answer)
    return str(r)