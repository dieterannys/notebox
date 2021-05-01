#!/usr/bin/env python3

import os
from dataclasses import dataclass
from typing import Dict, Any

from notebox.config import ContextTypeConfig
from notebox.context_provider.base import ContextProvider, ContextProviderItem
from notebox.note_folder import NoteFolder
from notebox.note import Note


class ContextType(NoteFolder):

    def __init__(self, config: ContextTypeConfig, root_folder: str, context_providers: Dict[str, ContextProvider]):
        self.name = config.name
        self.provider: ContextProvider = context_providers[config.context_provider.name]
        self.provider_collection: str = config.context_provider.collection
        self.title_format = config.title_format

        super().__init__(os.path.join(root_folder, self.name), is_reference=True)

    def get_uid_from_attributes(self, context_provider_item: ContextProviderItem):
        return f"{context_provider_item.service}-{context_provider_item.account}-{context_provider_item.uid}"

    def pull(self):
        super().pull()
        for provider_item in self.provider.get_items(self.provider_collection):
            note_title = self.title_format.format(**provider_item.__dict__, **provider_item.attributes)
            uid = self.get_uid_from_attributes(provider_item)
            try:
                note = self.notes_by_id[uid]
            except KeyError:
                note = self.notes.create(note_title, uid)
            note.provider_item = provider_item
            note.flagged = True

