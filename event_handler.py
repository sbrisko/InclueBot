"""
Slack chat-bot Lambda handler.
"""

import os
import logging
import urllib
import re
import boto3
import time
import uuid

dynamodb = boto3.resource('dynamodb')

# Grab the Bot OAuth token from the environment.
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Define the URL of the targeted Slack API resource.
# We'll send our replies there.
SLACK_URL = "https://slack.com/api/chat.postEphemeral"


def lambda_handler(data, context):
    """Handle an incoming HTTP request from a Slack chat-bot.
    """
    if "challenge" in data:
        return data["challenge"]
        
    # Grab the Slack event data.
    slack_event = data['event']
    
    # We need to discriminate between events generated by 
    # the users, which we want to process and handle, 
    # and those generated by the bot.
    if "bot_id" in slack_event:
        logging.warn("Ignore bot event")
    else:
        # Get the text of the message the user sent to the bot,
        text = slack_event["text"]
        term = ""
        output_text = ""

        # check it for words
        if len(re.findall( r'\bguys\b', text, re.IGNORECASE) ) > 0:
            term = 'guys'
            output_text = output_text + "Calling a group of women and men _'guys'_ can result in women feeling invisible or unwelcome. And if you're a straight guy about to say 'but *guys* is gender neutral!' consider all the guys you've dated lately?\n"
            output_text = output_text + "Try using _people_, _folks_, _group_, _gang_, or _honored mortals_ instead.\n"

        if len(re.findall( r'\bmaster\b', text, re.IGNORECASE) ) > 0:
            term = 'master'
            output_text = output_text + "Using the word _'master'_ in a context other than actual slavery can make a false equivalence that diminishes the harm done by slavery. In an American context, that harm includes lasting effects that have a direct, daily impact on the Americans descended from slaves and on people who look like them.\n"
            output_text = output_text + "Try using _primary_, _principal_, or _original_ instead.\n"

        if len(re.findall( r'\bslave\b', text, re.IGNORECASE) ) > 0:
            term = 'slave'
            output_text = output_text + "Using the word _'slave'_ in a context other than actual slavery can make a false equivalence that diminishes the harm done by slavery. In an American context, that harm includes lasting effects that have a direct, daily impact on the Americans descended from slaves and on people who look like them.\n"
            output_text = output_text + "Try using _secondary_, _redundant_, or _backup_ instead.\n"
        
        if len(re.findall( r'\blame\b', text, re.IGNORECASE) ) > 0:
            term = 'lame'
            output_text = output_text + "The use of the word _'lame'_ can result in people with certain disabilities feeling invisible or unwelcome.\n"
            output_text = output_text + "Try using _unwise_, _uncool_, or _hamstrung_ instead.\n"

        if len(re.findall( r'\bdumb\b', text, re.IGNORECASE) ) > 0:
            term = 'dumb'
            output_text = output_text + "The use of the word _'dumb'_ can result in people with certain disabilities feeling invisible or unwelcome.\n"
            output_text = output_text + "Try using _unwise_, _unproven_, or _obtuse_ instead.\n"

        if len(re.findall( r'\bcrazy\b', text, re.IGNORECASE) ) > 0:
            term = 'crazy'
            output_text = output_text + "The use of the word _'crazy'_ can result in people with certain disabilities feeling invisible or unwelcome.\n"
            output_text = output_text + "Try using _impractical_, _half-baked_, or _unusual_ instead.\n"

        if len(re.findall( r'\bboys\b', text, re.IGNORECASE) ) > 0:
            term = 'boys'
            output_text = output_text + "Calling an adult a child can be shaming and dismissive. We do it accidentally sometimes.\nThis is just a reminder to be thoughtful about what we're intending to communicate.\n"
        
        if len(re.findall( r'\bgirls\b', text, re.IGNORECASE) ) > 0:
            term = 'girls'
            output_text = output_text + "Calling an adult a child can be shaming and dismissive. We do it accidentally sometimes.\nThis is just a reminder to be thoughtful about what we're intending to communicate.\n"
        
        if len(output_text) > 0:
            # Get the ID of the channel where the message was posted.
            channel_id = slack_event["channel"]
            # Get the id of the user who sent the message    
            user = slack_event["user"]
            
            table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
            timestamp = int(time.time() * 1000)
            
            item = {
                    'id': str(uuid.uuid1()),
                    'term': term,
                    'original_text': text,
                    'timestamp': timestamp,
                    'channel': slack_event["channel"],
                }
            
                # write the hit to the database
            table.put_item(Item=item)
        
            # We need to send back four pieces of information:
            #     1. The reversed text (text)
            #     2. The userid of the person who sent the message
            #     2. The channel id of the private, direct chat (channel)
            #     3. The OAuth token required to communicate with 
            #        the API (token)
            # Then, create an associative array and URL-encode it, 
            # since the Slack API doesn't not handle JSON (bummer).
            data = urllib.parse.urlencode(
                (
                    ("token", BOT_TOKEN),
                    ("user", user),
                    ("channel", channel_id),
                    ("text", output_text)
                )
            )
            data = data.encode("ascii")
        
            # Construct the HTTP request that will be sent to the Slack API.
            request = urllib.request.Request(
                SLACK_URL, 
                data=data, 
                method="POST"
            )
            # Add a header mentioning that the text is URL-encoded.
            request.add_header(
                "Content-Type", 
                "application/x-www-form-urlencoded"
            )
            
            # Fire off the request!
            urllib.request.urlopen(request).read()

    # Everything went fine.
    return "200 OK"