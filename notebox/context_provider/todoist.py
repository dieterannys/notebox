#!/usr/bin/env python3
import re
from datetime import datetime

import todoist

from notebox.context_provider.base import ContextProvider, ContextProviderItem, ContextProviderItemType


class ContextProviderTodoist(ContextProvider):

    def __init__(self, params):
        self.client = todoist.TodoistAPI(params['api_key'])
        print(f"Connected to Todoist account {self.client.state['user']['email']}")

    @property
    def _project_name_by_id(self):
        return {p['id']: p['name'] for p in self.client.state['projects']}

    @property
    def _project_id_by_name(self):
        return {p['name']: p['id'] for p in self.client.state['projects']}

    @property
    def _label_name_by_id(self):
        return {p['id']: p['name'] for p in self.client.state['labels']}

    def _convert_to_item(self, raw):
        jira_codes = re.findall(r"[A-Z]+-[0-9]+", raw['content'])
        title = raw['content']
        created_time = datetime.fromisoformat(raw["date_added"][:-1])
        return ContextProviderItem(
            title=title,
            uid=raw["id"],
            collection=self._project_name_by_id[raw["project_id"]],
            account=self.client.state["user"]["email"],
            service="todoist",
            item_type=ContextProviderItemType.TASK,
            attributes=dict(
                tags=[self._label_name_by_id[label_id] for label_id in raw['labels']] + jira_codes,
                created_time=datetime.fromisoformat(raw["date_added"][:-1]),
            ),
            raw=raw,
        )

    def get_items(self, collection: str):
        self.client.sync()
        project_id = self._project_id_by_name[collection]
        return [self._convert_to_item(raw) for raw in self.client.state['items'] 
                if raw['project_id'] == project_id
                and raw['due'] is not None and datetime.now().strftime('%Y-%m-%d') >= raw['due'].get('date')[:10]
                and raw['checked'] == 0]

    def get_comments(self, task):
        return [n for n in self.client.state['notes'] if n['item_id'] == task.uid]

