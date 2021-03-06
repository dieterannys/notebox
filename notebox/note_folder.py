#!/usr/bin/env python3

import os
from datetime import datetime

from notebox.note import Note, NoteBody, NoteType


class MalformedNoteException(Exception):
    pass


class NoteFolder:
    '''Manages a folder of notes, and conversions between files and Note objects
    '''

    def __init__(self, path: str, note_type: NoteType, domain: str = None):
        self.path = os.path.abspath(path)
        self.notes = []
        self.note_type = note_type
        self.domain = domain

        self.pull()

    @property
    def notes_by_id(self):
        return {n.uid: n for n in self.notes}

    @property
    def notes_by_title(self):
        return {n.body.title: n for n in self.notes}

    @property
    def titles(self):
        return [n.body.title for n in self.notes]

    @property
    def uids(self):
        return [n.uid for n in self.notes]

    def create_path_if_not_exists(self):
        os.makedirs(self.path, exist_ok=True)

    def generate_uid(self):
        new_uid = datetime.now().strftime('%Y%m%d%H%M%S')
        if new_uid in self.uids:
            raise ValueError("UID already exists")
        return new_uid

    def create(self, title: str, custom_uid: str = None):
        uid = self.generate_uid() if custom_uid is None else custom_uid
        note = Note(
            uid=uid,
            folder_path=self.path,
            note_type=self.note_type,
            body=NoteBody(
                title=title,
            ),
            domain=self.domain,
        )
        note.push()
        self.notes.append(note)
        return note

    def pull(self):
        '''Read all available notes in path and store in notes list
        '''
        self.create_path_if_not_exists()
        self.notes = [
            Note.load(os.path.join(self.path, fn), self.note_type, self.domain)
            for fn in os.listdir(self.path)
            if fn.endswith(".md")
        ]

    def push(self):
        '''Write all notes in notes list to path
        '''
        self.create_path_if_not_exists()
        for note in self.notes:
            note.push()

