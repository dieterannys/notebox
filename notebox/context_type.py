#!/usr/bin/env python3

import os
from dataclasses import dataclass
from typing import Dict, Any

from notebox.config import ContextTypeConfig
from notebox.context_provider.base import ContextProvider, ContextProviderItem
from notebox.note_folder import NoteFolder
from notebox.note import Note


@dataclass
class Context:
    note: Note
    context_provider_item: ContextProviderItem = None


class ContextType:

    def __init__(self, config: ContextTypeConfig, root_folder: str, context_providers: Dict[str, ContextProvider]):
        self.name = config.name
        self.notes = NoteFolder(os.path.join(root_folder, self.name))
        self.context_provider: ContextProvider = context_providers[config.context_provider.name]
        self.context_provider_collection: str = config.context_provider.collection
        
        self.contexts = []
        self.pull()

    @property
    def contexts_by_note_id(self):
        return {c.note.uid: c for c in self.contexts}

    def get_uid_from_attributes(self, context_provider_item: ContextProviderItem):
        return f"{context_provider_item.service}-{context_provider_item.account}-{context_provider_item.uid}"

    def pull(self):
        self.contexts = []
        for context_provider_item in self.context_provider.get_items(self.context_provider_collection):
            uid = self.get_uid_from_attributes(context_provider_item)
            try:
                note = self.notes.notes_by_id[uid]
            except KeyError:
                note = self.notes.create(context_provider_item.refnote_title, uid)
            self.contexts.append(Context(
                note=note,
                context_provider_item=context_provider_item
            ))

