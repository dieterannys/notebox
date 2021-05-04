#!/usr/bin/env python3

import os
from typing import Dict

from notebox.config import ContextTypeConfig
from notebox.context_provider.base import ContextProvider, ContextProviderItem
from notebox.note_folder import NoteFolder


class ContextType(NoteFolder):

    def __init__(self, config: ContextTypeConfig, root_folder: str, context_providers: Dict[str, ContextProvider]):
        self.name = config.name

        if config.context_provider is not None:
            self.provider: ContextProvider = context_providers[config.context_provider.name]
            self.provider_collection: str = config.context_provider.collection
        else:
            self.provider = None
            self.provider_collection = None
        self.title_format = config.title_format

        super().__init__(os.path.join(root_folder, self.name), is_reference=True)

    def get_uid_from_attributes(self, context_provider_item: ContextProviderItem):
        return f"{context_provider_item.service}-{context_provider_item.account}-{context_provider_item.uid}"

    def pull(self):
        super().pull()

        if self.provider is None:
            return

        for provider_item in self.provider.get_items(self.provider_collection):
            note_title = self.title_format.format(**provider_item.__dict__, **provider_item.attributes)
            uid = self.get_uid_from_attributes(provider_item)
            try:
                note = self.notes_by_id[uid]
                note.body.title = note_title
                note.push()
            except KeyError:
                note = self.create(note_title, uid)
            note.provider_item = provider_item
            note.flagged = True

