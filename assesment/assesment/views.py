from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport import requests
from google.oauth2.credentials import Credentials
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Constants for OAuth2 credentials and API scopes
CLIENT_ID = '637823788808-u6c068kv5lbepcic2jd2bnhqufm5f1ov.apps.googleusercontent.com'
CLIENT_SECRET = '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'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
REDIRECT_URI = 'http://localhost:8000/rest/v1/calendar/redirect/'


class GoogleCalendarInitView(View):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            'D:\\covin\\assesment\\client_secret_637823788808-u6c068kv5lbepcic2jd2bnhqufm5f1ov.apps.googleusercontent.com.json',
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,
        )
        authorization_url, state = flow.authorization_url( access_type='offline',include_granted_scopes='true')
        request.session['state'] = state
        return redirect(authorization_url)

class GoogleCalendarRedirectView(View):
    def get(self, request):
        state = request.session['state']
        flow = Flow.from_client_secrets_file(
            'D:\\covin\\assesment\\client_secret_637823788808-u6c068kv5lbepcic2jd2bnhqufm5f1ov.apps.googleusercontent.com.json',
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,
            state=state
        )
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        credentials = flow.credentials

        # Use the obtained credentials to retrieve events from the user's calendar
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary').execute()
        events = events_result.get('items', [])

        # Process the events as per your requirements
        for event in events:
            print(event)

        return HttpResponse("Events retrieved successfully!")