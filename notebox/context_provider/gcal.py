#!/usr/bin/env python3

import os
import pickle
from datetime import datetime, timedelta
from typing import Dict, Any

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from notebox.context_provider.base import ContextProvider, ContextProviderItem


class ContextProviderGcal(ContextProvider):

    def __init__(self, params):
        username = params['username']
        creds_fp = params['credentials_json_path']

        token_fp = os.path.splitext(creds_fp)[0] + ".pickle"
        creds = None
        if os.path.exists(token_fp):
            with open(token_fp, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_fp,
                    ["https://www.googleapis.com/auth/calendar.readonly"]
                )
                creds = flow.run_local_server(port=0)
            with open(token_fp, 'wb') as token:
                pickle.dump(creds, token)

        self.calendar = build('calendar', 'v3', credentials=creds)
        self.username = username

        print(f'Connected to Gcal account {self.username}')

    def _convert_to_item(self, raw, collection):
        title = raw['summary'].strip()
        start_time = datetime.fromisoformat(raw['start']['dateTime'])
        end_time = datetime.fromisoformat(raw['end']['dateTime'])
        return ContextProviderItem(
            title=title,
            uid=raw["id"],
            collection=collection,
            account=self.username,
            service="gcal",
            start_time = start_time,
            end_time = end_time,
            raw=raw,
        )

    def get_items(self, filters: Dict[str, Any]):
        if set(filters.keys()) != {"calendar"}:
            raise ValueError("Gcal filters should contain a single key 'calendar'")
        start = datetime.now().replace(hour=0, minute=0, second=0)
        end = start + timedelta(days=1)
        events_result = self.calendar.events().list(
            calendarId=filters['calendar'],
            timeMin=start.isoformat() + 'Z',
            timeMax=end.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return [self._convert_to_item(raw, filters['calendar']) for raw in events_result.get("items", [])]

