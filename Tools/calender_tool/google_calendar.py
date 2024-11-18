from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timezone, timedelta 

class GoogleCalendarManager:
    def __init__(self, credentials_path, calendar_id):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.credentials_path = credentials_path
        self.calendar_id = calendar_id  # Store the calendar ID
        self.service = None
        
    def authenticate(self):
        """Authenticate using service account credentials."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=self.SCOPES
            )
            
            # Build the service
            self.service = build('calendar', 'v3', credentials=credentials)
            return True
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False

    def list_upcoming_events(self, num_days : int = 7):
        """List upcoming events from the specified calendar."""
        # Use timezone-aware datetime object
        now = datetime.now(timezone.utc)
        try:
            events_result = self.service.events().list(
                calendarId=self.calendar_id,  # Use the specified calendar ID
                timeMin=now.isoformat(),
                timeMax = (now + timedelta(days=num_days)).isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            return events_result.get('items', [])
        except Exception as e:
            print(f'Error listing events: {e}')
            return []

    def add_event(self, summary, description, start_time, end_time, timezone='UTC'):
        """Add an event to the specified calendar."""

        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': timezone,
            },
        }

        try:
            event = self.service.events().insert(
                calendarId=self.calendar_id,  # Use the specified calendar ID
                body=event
            ).execute()
            return True
        except Exception as e:
            print(f'Error creating event: {e}')
            return None

    def delete_event(self, event_id):
        """Delete an event from the specified calendar."""
        try :
            self.service.events().delete(
                calendarId=self.calendar_id,  # Use the specified calendar ID
                eventId=event_id
            ).execute()
            return True
        
        except Exception as e:
            print(f'Error deleting event: {e}')
            return False