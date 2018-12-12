import logging
import os
from flask import Flask
from flask_ask import Ask, request, session, question, statement
from typeform import get_questions, get_responses, get_average_rating, count_true_false


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    speech_text = 'Welcome to the Alexa Typeform Skill. You can ask me what your user feedback is, or you can ask me to remind you what the questions are.'
    return question(speech_text).reprompt(speech_text).simple_card('app', speech_text)

@ask.intent('GetQuestions')
def return_questions():
    questions = get_questions()
    speech_text = 'The questions you asked are. '
    for question in questions:
        speech_text = speech_text + ' ' + str(question['text'])
    return statement(speech_text).simple_card('Questions', speech_text)

@ask.intent('CustomerFeedback')
def return_feedback():
    questions = get_questions()
    responses = get_responses()
    i=0
    speech_text = "You have {} responses in total. Here are the answers: ".format(responses['number_responses'])
    for question in questions:
        print("Question: {}".format(question['text']))
        if question['type'] == 'rating':
            average_rating = get_average_rating(responses['results'], question['id'])
            answer = "Your average rating is {} .".format(average_rating)
        elif question['type'] == 'opinion_scale' :
            average_rating = get_average_rating(responses['results'], question['id'])
            answer = "The average score is {} out of 5.".format(average_rating)
        else:
            count = count_true_false(responses['results'], question['id'])
            answer = "{} out of {} said yes.".format(count[0], count[0] + count[1])
        print("The answer is: {} (type: {})".format(answer, type(answer)))
        speech_text = speech_text + " " + question['text'] + " " + answer + " " 
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
    return_questions()
    app.run(debug=True)
