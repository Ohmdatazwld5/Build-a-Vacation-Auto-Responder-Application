#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import os
import random
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from google.auth.transport.requests import Request

# Define the required scopes for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Load credentials from credentials.json
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

#If no valid credentials are found, authenticate the user
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        
# Save the credentials for the next run
with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Create a Gmail service instance
service = build('gmail', 'v1', credentials=creds)

def check_emails():
    # Get the total number of emails in the inbox
    inbox = service.users().labels().get(userId='me', id='INBOX').execute()
    total_emails = inbox['messagesTotal']
    print(f"You have {total_emails} emails in your inbox")
    
# Get a list of messages in the inbox
messages = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()

for message in messages['messages']:
        # Get the message data
        message_data = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = message_data['payload']
        thread_id = message_data['threadId']

        sent_threads = []

def check_emails():
    if thread_id in sent_threads:
        print('Vacation response has already been sent to this thread. Skipping...')

# Call the function
check_emails()

headers = payload['headers']
has_replies = any(header['name'] == 'In-Reply-To' for header in headers)

if not has_replies:
    print('No prior replies found. Sending reply now...')
    
    # Check if a vacation response has already been sent to this thread
    if thread_id in sent_threads:
        print('Vacation response has already been sent to this thread. Skipping...')

# Send a reply to the message
import base64
email_from = next(header['value'] for header in headers if header['name'] == 'From')
email_subject = next(header['value'] for header in headers if header['name'] == 'Subject')
reply_message = f"From: vacationmailsender@gmail.com\r\n"
reply_message += f"To: {email_from}\r\n"
reply_message += f"Subject: RE: {email_subject}\r\n"
reply_message += f"\r\n"
reply_message += f"Thank you for your email. I am currently out of office on vacation and will not be able to respond until I return. I appreciate your patience and look forward to getting back to you soon."

service.users().messages().send(
        userId='me',
        body={
            'raw': base64.urlsafe_b64encode(reply_message.encode('utf-8')).decode('utf-8'),
            'threadId': thread_id
        }
    ).execute()     

# Generate a random interval between 45 to 120 seconds
interval = random.randint(45, 120)
print(f"Next check in {interval} seconds")

# Repeat the tasks in the random interval
time.sleep(interval)
check_emails()


# In[ ]:




