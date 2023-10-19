from __future__ import print_function
import json
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_event(calendar_id, summary, start_datetime, end_datetime):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:    
        service = build('calendar', 'v3', credentials=creds)

    except HttpError as error:
        print('An error occurred: %s' % error)

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_datetime,
            'timeZone': 'Asia/Dubai',
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': 'Asia/Dubai',
        },
    }

    try: 
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        #print('Event created: %s' % (event.get('htmlLink')))
    except Exception as e:
        error = json.loads(e.content)
        print(f'Error details: {error}')

def delete_event(calendar_id):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    try:
        summary = f'Prayer Time Event'
        service = build('calendar', 'v3', credentials=creds)
        events_result = service.events().list(calendarId=calendar_id, q=summary).execute()
        events = events_result.get('items', [])

        if not events:
            print('No events found.')
        else:
            for event in events:
                event_id = event['id']
                print(f'Deleting event with summary: {summary}, id: {event_id}')
                service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
                print(f'Event with id {event_id} deleted successfully.')

    except HttpError as error:
        print('An error occurred: %s' % error)

def main():     
    # Google Calendar ID (can be obtained from Google Calendar settings)
    calendar_id = 'haskhr@hotmail.com'
    #delete_event(calendar_id)

    # Read event data from the JSON file
    with open('prayer_times.json', 'r') as file:
        prayer_times_data = json.load(file)

    # Iterate through the prayer times data and create events
    for prayer_date, prayer_times in prayer_times_data.items():
    # Extract prayer timings excluding Shurooq
        prayer_timings = {key: value for key, value in prayer_times.items() if key != 'Shurooq'}
    
    # Create events for each prayer timing
        for prayer_name ,prayer_time in prayer_timings.items():
            start_time = datetime.datetime.strptime(f'{prayer_date} {prayer_time}', '%Y-%m-%d %H:%M')
            end_time = start_time + datetime.timedelta(minutes=10)
            summary = f'Prayer Time - {prayer_name}'
            start_datetime = start_time.strftime('%Y-%m-%dT%H:%M:%S+04:00')
            end_datetime = end_time.strftime('%Y-%m-%dT%H:%M:%S+04:00')
        
        # Here, you can use the `create_event` function to add the event to Google Calendar
            create_event(calendar_id, summary, start_datetime, end_datetime)
        # For demonstration purposecas, print the event details
        # print(f'Event Summary: {summary}')
        # print(f'Start Time: {start_datetime}')
        # print(f'End Time: {end_datetime}')
        # print('---')

if __name__ == '__main__':
    main()

