#!/usr/bin/env python3

import os
from typing import Dict

from notebox.config import ContextFolderConfig
from notebox.context_provider.base import ContextProvider, ContextProviderItem
from notebox.note_folder import NoteFolder
from notebox.note import NoteType


class ContextFolder(NoteFolder):

    def __init__(self, config: ContextFolderConfig, path: str, context_providers: Dict[str, ContextProvider], note_type=NoteType, domain: str = None):
        if config is not None:
            self.provider: ContextProvider = context_providers[config.provider]
            self.provider_filter: str = config.filter
            self.title_format = config.title_format
        else:
            self.provider = None
            self.provider_filter = None
            self.title_format = "{title}"

        super().__init__(path, note_type, domain)

    def get_uid_from_attributes(self, context_provider_item: ContextProviderItem):
        return "-".join([
            str(e) 
            for e in [
                context_provider_item.service, 
                context_provider_item.account, 
                context_provider_item.uid
            ] 
            if e is not None
        ])

    def pull(self):
        super().pull()

        if self.provider is None:
            return

        for provider_item in self.provider.get_items(self.provider_filter):
            note_title = self.title_format.format(**provider_item.__dict__)
            uid = self.get_uid_from_attributes(provider_item)
            try:
                note = self.notes_by_id[uid]
                note.body.title = note_title
                note.push()
            except KeyError:
                note = self.create(note_title, uid)
            note.provider_item = provider_item
            note.flagged = True

