#!/usr/bin/env python3
import re
from datetime import datetime
from typing import Dict, Any
from fnmatch import fnmatch

import todoist

from notebox.context_provider.base import ContextProvider, ContextProviderItem


class ContextProviderTodoist(ContextProvider):

    def __init__(self, params):
        self.client = todoist.TodoistAPI(params['api_key'])
        self.client.sync()
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

    @property
    def _section_name_by_id(self):
        return {p['id']: p['name'] for p in self.client.state['sections']}

    def _convert_to_item(self, raw):
        title = raw['content']
        created_time = datetime.fromisoformat(raw["date_added"][:-1])

        tags = [self._label_name_by_id[label_id] for label_id in raw['labels']]

        jira_codes = re.findall(r"[A-Z]+-[0-9]+", raw['content'])
        tags.extend(jira_codes)

        if raw['section_id'] is not None:
            tags.append(self._section_name_by_id[raw['section_id']])

        return ContextProviderItem(
            title=title,
            uid=raw["id"],
            collection=self._project_name_by_id[raw["project_id"]],
            account=self.client.state["user"]["email"],
            service="todoist",
            tags=tags,
            created_time=datetime.fromisoformat(raw["date_added"][:-1]),
            raw=raw,
        )

    @property
    def all_items(self):
        self.client.sync()
        return [
            self._convert_to_item(raw) for raw in self.client.state['items']
            if raw['checked'] == 0
            and raw['parent_id'] is None
        ] 

    def get_items(self, filters: Dict[str, Any]):
        items = self.all_items
        for k, v in filters.items():
            if k == "project":
                if isinstance(v, str):
                    items = [i for i in items if fnmatch(i.collection, v)]
                elif isinstance(v, list):
                    items = [i for i in items if i.collection in v]
            elif k == "priority":
                if isinstance(v, str):
                    items = [i for i in items if i.raw['priority'] == v]
                elif isinstance(v, list):
                    items = [i for i in items if i.raw['priority'] in v]
            else:
                raise NotImplementedError(f"Todoist filter {k} not implemented")
        return items

    def get_comments(self, task):
        return [n for n in self.client.state['notes'] if n['item_id'] == task.uid]

