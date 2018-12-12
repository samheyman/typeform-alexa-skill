import time
import json
from urllib import request, parse
from collections import namedtuple
import os

base_url = 'https://api.typeform.com/forms/'

def api_call(url):
    header = {
		'Authorization': 'Bearer ' + os.environ['TYPEFORM_TOKEN']
	}
    req = request.Request(url, headers=header)
    try:
        response = request.urlopen(req)
        return json.load(response)
    except:
        print("Error with API call")
        return None

def get_questions():
    questions = []
    response = api_call(base_url + os.environ['FORM_ID'])
    for item in response['fields']:
        question = {}
        question['id'] = item['id']
        question['text'] = item['title']
        question['type'] = item['type']
        questions.append(question)
    return questions

def get_responses():
    responses = []
    response = api_call(base_url + os.environ['FORM_ID'] + '/responses')
    for item in response['items']:
        if 'answers' in item:
            for answer in item['answers']:
                entry = {}
                entry['id'] = answer['field']['id']
                entry['type'] = answer['field']['type']
                entry['value'] = answer['number'] if answer['field']['type'] == 'rating' else answer['boolean']
                responses.append(entry)
    return responses

def get_average_rating(responses, question_id):
    sum_ratings = sum(item['value'] for item in responses if item['id'] == question_id)
    number_ratings = sum(1 for item in responses if item['id'] == question_id)
    average_rating = round(sum_ratings / number_ratings, 1)
    return average_rating

def count_true_false(responses, question_id):
    true_false_count = namedtuple('NumberTrue', 'NumberFalse')
    number_true = sum(1 for item in responses if item['id'] == question_id and item['value'])
    number_false = sum(1 for item in responses if item['id'] == question_id and not item['value'])
    total = sum(1 for item in responses if item['id'] == question_id)
    true_false_count = (number_true, number_false)
    # print("True: {}, False {}, Total {}".format(number_true, number_false, total))
    return true_false_count

# if __name__ == "__main__":
#     questions = get_questions()
#     responses = get_responses()
#     for question in questions:
#         print("Question: {}".format(question['text']))
#         if question['type'] == 'rating':
#             average_rating = get_average_rating(responses, question['id'])
#             print("Average rating: {}".format(average_rating))
#         else:
#             count = count_true_false(responses, question['id'])
#             print("{} out of {} said yes.".format(count[0], count[0] + count[1]))