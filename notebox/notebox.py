#!/usr/bin/env python3

import os
import subprocess

from notebox.config import Config
from notebox.note_folder import NoteFolder
from notebox.note import Note, NoteType, Link
from notebox.context_provider import context_provider_factory
from notebox.context_type import ContextType


def refresh(f):
    def wrapper(self, *args, **kwargs):
        self.zettels.pull()
        res = f(self, *args, **kwargs)
        self.zettels.push()
        return res
    return wrapper


class Notebox:

    ZETTELS_DIR = "zettels"
    CONTEXT_DIR = "context"

    def __init__(self, config: Config):
        self.name = config.name
        self.path = config.path
        self.editor = config.editor

        self.zettels = NoteFolder(os.path.join(self.path, self.ZETTELS_DIR))

        self.context_providers = {
            context_provider_config.name: context_provider_factory(context_provider_config)
            for context_provider_config in config.context_providers
        }

        self.context_types = {
            context_type_config.name: ContextType(context_type_config, os.path.join(self.path, self.CONTEXT_DIR), self.context_providers)
            for context_type_config in config.context_types
        }

    def edit_note(self, note: Note):
        subprocess.Popen([*self.editor, note.filepath])

    def link(self, note1: Note, note2: Note):
        note1.pull()
        note2.pull()

        for note_from, note_to in [(note1, note2), (note2, note1)]:
            link = Link(note_to.body.title, os.path.relpath(note_to.filepath, note_from.folder_path))

            if note_to.note_type == NoteType.ZETTEL:
                links = note_from.body.links
            elif note_to.note_type == NoteType.CONTEXT:
                links = note_from.body.references

            if link.path not in [l.path for l in links]:
                links.append(link)

        note1.push()
        note2.push()

    def get_or_create_zettel_by_title(self, title: str):
        try:
            return self.zettels.notes_by_title[title]
        except KeyError:
            return self.zettels.create(title)


