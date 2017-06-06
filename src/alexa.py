# This attempts to be (more or less) the simplest possible hello world Alexa skill...
from __future__ import print_function
import random
import requests

# We'll start with a couple of globals...
CardTitlePrefix = "Greeting"

# --------------- Helpers that build all of the responses ----------------------

def get_destination():
    headers = {
        'Authorization': 'Bearer: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImVtYWlsIjoiZ3Vlc3RAYmxhc3RhcHAuaW8ifQ.N4QVBH42-67xKY0sBDqahL9copEiutE1HFm6mAebm5k',
        'Content-Type': 'application/json'
    }

    response = requests.get('https://calm-sands-26146.herokuapp.com/api/v1/destination', headers=headers)

    return response.json()

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    """
    Build a speechlet JSON representation of the title, output text,
    reprompt text & end of session
    """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': CardTitlePrefix + " - " + title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    """
    Build the full response JSON from the speechlet response
    """
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    session_attributes = {}
    card_title = "Hello"
    speech_output = "Welcome to the Hello World demonstration... Ask me to say hello."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I'm sorry - I didn't understand. You should ask me to say hello..."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def say_hello():
    """
    Return a lunch phrase...
    """
    card_title = "Hello"
    one = random.choice(['krog street market', 'bell street burritos', 'victory','superica', 'ponce city market', 'Daddy D'])
    greeting_string = "Hello! This is Guy Fieri and we are going to eat at %s in flavor town." % one
    return build_response({}, build_speechlet_response(card_title, greeting_string, "Ask me to say hello...", True))

def say_hello_dinner():
    """
    Return a dinner phrase...
    """
    card_title = "Hello"
    two = random.choice(['krog street market', 'bell street burritos', 'victory','superica', 'ponce city market', 'Daddy D'])
    greeting_string = "Hello! This is Guy Fieri and we are going to eat at %s in flavor town." % two
    return build_response({}, build_speechlet_response(card_title, greeting_string, "Ask me to say hello...", True))



# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want """
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    # Dispatch to your skill's intent handlers

    if intent_name == "lunch":
        destination = get_destination()
        return destination.name
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session. Is not called when the skill returns should_end_session=true """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])

    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])

    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
