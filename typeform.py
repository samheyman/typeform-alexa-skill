import logging
import os
from flask import Flask
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    speech_text = 'Welcome to the Alexa Skills Kit, you can say hello'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('Questions')
def return_questions():
    questions = ['How would you rate your stay?', 'Would you come again?', 'Would you recommend us?']
    speech_text = 'The questions you asked are'
    for question in questions:
        speech_text = speech_text + question
    return statement(speech_text).simple_card('Questions', speech_text)

@ask.intent('CustomerFeedback')
def return_feedback():
    questions = [" How would you rate your stay? ", ". Would you come again? ", " Would you recommend us? "]
    responses = []
    i = 1
    responses.append(". 5 ")
    responses.append(" Your average rating is 3 point 5. ")
    responses.append(" 2 out of 5 said yes. ")
    responses.append(" 3 out of 5 said yes. ")
    speech_text = "You have had {} responses in total. Here are the answers: ".format(responses[0])
    for question in questions:
        speech_text = " " + speech_text + " " + question + " " + responses[i] + " " 
        i+=1
    return statement(speech_text).simple_card('Responses', speech_text)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    app.run(debug=True)
