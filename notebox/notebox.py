#!/usr/bin/env python3

import os
import subprocess
from dataclasses import dataclass

from notebox.config import Config, ContextFolderConfig
from notebox.note_folder import NoteFolder
from notebox.note import Note, NoteType, Link
from notebox.context_provider import context_provider_factory
from notebox.context_provider.daily import ContextProviderDaily
from notebox.context_folder import ContextFolder


def refresh(f):
    def wrapper(self, *args, **kwargs):
        self.zettel.pull()
        res = f(self, *args, **kwargs)
        self.zettel.push()
        return res
    return wrapper


class Notebox:

    def __init__(self, config: Config):
        self.path = config.path
        self.editor = config.editor

        self.context_providers = {
            context_provider_config.name: context_provider_factory(context_provider_config)
            for context_provider_config in config.context_providers
        }
        self.context_providers['daily'] = ContextProviderDaily()

        self.zettel = NoteFolder(os.path.join(self.path, "zettel"), NoteType.ZETTEL)
        self.source = ContextFolder(config.source, os.path.join(self.path, "source"), self.context_providers, NoteType.SOURCE)
        # TODO Add dailies
        self.daily = ContextFolder(ContextFolderConfig('daily', "{title}", dict()), os.path.join(self.path, "daily"), self.context_providers, NoteType.DAILY)

        self.domains = {
            domain_config.name: dict(
                event=ContextFolder(domain_config.event, os.path.join(self.path, domain_config.name, "event"), self.context_providers, NoteType.EVENT, domain_config.name),
                project=ContextFolder(domain_config.project, os.path.join(self.path, domain_config.name, "project"), self.context_providers, NoteType.PROJECT, domain_config.name),
                zettel=NoteFolder(os.path.join(self.path, domain_config.name, "zettel"), NoteType.ZETTEL, domain_config.name)
            )
            for domain_config in config.domains
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
            else:
                links = note_from.body.references

            if link.path not in [l.path for l in links]:
                links.append(link)

        note1.push()
        note2.push()

    @property
    def folders(self):
        return [
            self.zettel,
            self.source,
            self.daily,
            *[
                note_folder
                for domain in self.domains.values()
                for note_folder in domain.values()
            ]
        ]

    @property
    def folder_tree(self):
        return dict(
            zettel = self.zettel,
            source = self.source,
            daily = self.daily,
            **{
                domain: {
                    name: folder
                    for name, folder in folders.items()
                }
                for domain, folders in self.domains.items()
            }
        )

    def clean(self):
        for folder in self.folders:
            folder.pull()
            os.chdir(folder.path)
            print(f"Removing empty notes in {folder.path}: ", end='')
            for note in folder.notes:
                if note.is_empty:
                    print(".", end='')
                    note.delete()
                    continue
            print('')

