#!/usr/bin/env python3

import os
import re
from enum import Enum
from dataclasses import dataclass, field
from typing import List

import yaml

from notebox.context_provider.base import ContextProviderItem


LINKS_HEADER = "**Links**"
REFERENCES_HEADER = "**References**"


@dataclass(eq=True, frozen=True)
class Link:
    title: str
    path: str


class NoteType(Enum):
    ZETTEL = 1
    CONTEXT = 2


@dataclass
class NoteBody:

    # Front matter
    title: str
    # Content
    content: str = ""
    #  Footer
    links: List[Link] = field(default_factory=list)
    references: List[Link] = field(default_factory=list)

    @classmethod
    def from_string(cls, raw_content):
        blocks = raw_content.split('---')

        # Front matter
        if blocks[0] != '':
            raise MalformedNoteException(filepath)
        front_matter_raw = yaml.load(blocks[1], Loader=yaml.FullLoader)
        title = front_matter_raw['title']

        # Footer
        link_pattern = re.compile(r"\[(.+)\]\((.+)\)")
        links = []
        references = []
        has_footer = True
        in_links = False
        in_references = False
        for n, line in enumerate([l for l in blocks[-1].strip().split('\n') if l != '']):
            line = line.strip()
            if n == 0 and line != LINKS_HEADER and line != REFERENCES_HEADER:
                has_footer = False
                break
            elif line== LINKS_HEADER:
                in_links = True
                in_references = False
            elif line == REFERENCES_HEADER:
                in_links = False
                in_references = True
            else:
                m = link_pattern.search(line)
                if not m:
                    continue
                link = Link(m.groups()[0], m.groups()[1])
                if in_links:
                    links.append(link)
                elif in_references:
                    references.append(link)

        # Content
        content = "---".join(blocks[2:-1] if has_footer else blocks[2:]).strip()

        return cls(
            title=title,
            content=content,
            links=links,
            references=references
        )

    def to_string(self):
        lines = [
            f"---",
            f"title: \"{self.title}\"",
            f"---",
            f"",
            self.content,
        ]
        if len(self.links) > 0 or len(self.references) > 0:
            lines.append(f"\n---")
        if len(self.links) > 0:
            lines.append(f"\n{LINKS_HEADER}\n")
            for link in self.links:
                lines.append(f"- [{link.title}]({link.path})")
        if len(self.references) > 0:
            lines.append(f"\n{REFERENCES_HEADER}\n")
            for link in self.references:
                lines.append(f"- [{link.title}]({link.path})")
        return "\n".join(lines)


@dataclass
class Note:
    uid: str
    folder_path: str
    note_type: NoteType
    body: NoteBody
    provider_item: ContextProviderItem = None
    flagged: bool = False

    @property
    def filepath(self):
        return os.path.join(self.folder_path, self.uid + ".md")

    @property
    def is_empty(self):
        return len(self.body.content) == 0 and len(self.body.links) == 0 and len(self.body.references) == 0

    @classmethod
    def load(cls, filepath, note_type):
        with open(filepath) as f:
            raw_content = f.read()
        return cls(
            uid=os.path.split(os.path.splitext(filepath)[0])[-1],
            folder_path=os.path.abspath(os.path.dirname(filepath)),
            note_type=note_type,
            body=NoteBody.from_string(raw_content)
        )

    def pull(self):
        with open(self.filepath) as f:
            raw_content = f.read()
        self.body = NoteBody.from_string(raw_content)

    def push(self):
        with open(self.filepath, 'w') as f:
            f.write(self.body.to_string())

    def delete(self):
        os.remove(self.filepath)

