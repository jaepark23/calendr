import os.path
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ..models.calendar import Calendar

load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SECRET_KEY = os.getenv("GOOGLE_SECRET_KEY")
SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/calendar.events"]
TOKEN_URI = "https://oauth2.googleapis.com/token"

def verify_credentials(access_token : str, refresh_token : str) -> Credentials:
  """
  Verifiys Google credentials and returns Google Credentials. 

  access_token (str) : token used to verify user, sent from cookies 
  refresh_token (str) : token used for access token refresh, sent from cookies 

  Returns:
  (Credentials) : used to verify user later on
  """
  creds = Credentials(token=access_token, refresh_token=refresh_token, token_uri=TOKEN_URI, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

  if creds.expired and creds.refresh_token:
      creds.refresh(Request())

  return creds
  
def add_events_to_google_calendar(calendar : Calendar | dict, access_token : str, refresh_token : str) -> bool:
    """
    Constructs JSON from Calendar object and pushes it to Google Calendar. 

    calendar (Calendar | dict) : Calendar object or dictionary containing all events from a single PDF.
    access_token (str) : token used to verify user, sent from cookies 
    refresh_token (str) : token used for access token refresh, sent from cookies 

    Returns:
    (bool) : success or fail
    """

    creds = verify_credentials(access_token, refresh_token)
    
    try:
        service = build("calendar", "v3", credentials=creds)
        if type(calendar) != dict:
            calendar = calendar.dict()
        for homework in calendar['homework']:
            homework_event = {
              'summary': calendar['course_number'] + " " + homework['name'],
              'description': "Type:" + homework['type'],
              'start': {
                'dateTime': homework['deadline'],
                'timeZone': 'America/Chicago',
              },
              'end': {
                'dateTime': homework['deadline'],
                'timeZone': 'America/Chicago',
              }
            }
            service.events().insert(calendarId='primary', body=homework_event).execute()
        for exam in calendar['exams']:
            exam_event = {
              'summary': calendar['course_number'] + " " + exam['name'],
              'description': "Type:" + exam['type'],
              'start': {
                'dateTime': exam['deadline'],
                'timeZone': 'America/Chicago',
              },
              'end': {
                'dateTime': exam['deadline'],
                'timeZone': 'America/Chicago',
              }
            }
            service.events().insert(calendarId='primary', body=exam_event).execute()
            print("added event")
        for lab in calendar['labs']:
            lab_event = {
              'summary': calendar['course_number'] + " " + lab['name'],
              'description': "Type:" + lab['type'],
              'start': {
                'dateTime': lab['deadline'],
                'timeZone': 'America/Chicago',
              },
              'end': {
                'dateTime': lab['deadline'],
                'timeZone': 'America/Chicago',
              }
            }
            service.events().insert(calendarId='primary', body=lab_event).execute()
            print("added event")
        for project in calendar['projects']:
            project_event = {
              'summary': calendar['course_number'] + " " + project['name'],
              'description': "Type:" + project['type'],
              'start': {
                'dateTime': project['deadline'],
                'timeZone': 'America/Chicago',
              },
              'end': {
                'dateTime': project['deadline'],
                'timeZone': 'America/Chicago',
              }
            }
            service.events().insert(calendarId='primary', body=project_event).execute()
            print("added event")
        for quiz in calendar['quizzes']:
            quiz_event = {
              'summary': calendar['course_number'] + " " + quiz['name'],
              'description': "Type:" + quiz['type'],
              'start': {
                'dateTime': quiz['deadline'],
                'timeZone': 'America/Chicago',
              },
              'end': {
                'dateTime': quiz['deadline'],
                'timeZone': 'America/Chicago',
              }
            }
            service.events().insert(calendarId='primary', body=quiz_event).execute()
            print("added event")
        for other in calendar['other']:
            other_event = {
              'summary': calendar['course_number'] + " " + other['name'],
              'description': "Type:" + other['type'],
              'start': {
                'dateTime': other['deadline'],
                'timeZone': 'America/Chicago',
              },
              'end': {
                'dateTime': other['deadline'],
                'timeZone': 'America/Chicago',
              }
            }
            service.events().insert(calendarId='primary', body=other_event).execute()
            print("added event")

    except HttpError as error:
        print(f"An error occurred: {error}")
