import tweepy
import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
GOOGLE_CREDS= 'credentials.json'


# Twitter API credentials
# todo: Fix with secrets


# Gmail API credentials
creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            GOOGLE_CREDS, SCOPES
        )
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

# Get the list of unread emails
service = build("gmail", "v1", credentials=creds)
results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
messages = results.get('messages', [])

for message in messages:
    msg_id = message['id']
    msg = service.users().messages().get(userId='me', id=message['id']).execute()
    subject = [header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'][0]
    body = msg['snippet']

    # Tweet the email content
    tweet_content = f"New email received: {subject}\n\n{body}\n\n{int(time.time() * 1000)}"
    print(tweet_content)
    client = tweepy.Client(consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token=access_token,
                    access_token_secret=access_token_secret)

    response = client.create_tweet(text=tweet_content)
    # Mark the email as read
    service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()

import tweepy
import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
GOOGLE_CREDS= 'credentials.json'


# Twitter API credentials
# todo: Fix with secrets


# Gmail API credentials
creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            GOOGLE_CREDS, SCOPES
        )
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

# Get the list of unread emails
service = build("gmail", "v1", credentials=creds)
results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
messages = results.get('messages', [])

for message in messages:
    msg_id = message['id']
    msg = service.users().messages().get(userId='me', id=message['id']).execute()
    subject = [header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'][0]
    body = msg['snippet']

    # Tweet the email content
    tweet_content = f"New email received: {subject}\n\n{body}\n\n{int(time.time() * 1000)}"
    print(tweet_content)
    client = tweepy.Client(consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token=access_token,
                    access_token_secret=access_token_secret)

    response = client.create_tweet(text=tweet_content)
    # Mark the email as read
    service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
