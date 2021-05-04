#!/usr/bin/env python3

import sys
import os
import subprocess
from dataclasses import dataclass
from typing import List, Any, Callable

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion 

from notebox.notebox import Notebox
from notebox.note_folder import NoteFolder
from notebox.config import Config
from notebox.context_provider.base import ContextProviderItemType
from notebox.note import NoteType


@dataclass
class Command:
    name: str
    func: Callable
    argopts: Any = None


class NoteCompleter(Completer):

    STYLE_BG_DEFAULT = "bg:#BBBBBB"
    STYLE_BG_FLAGGED = "bg:ansiwhite"

    STYLE_FG = "fg:#333333"
    STYLE_FG_SELECTED = "fg:ansiblack bold"

    def __init__(self, commands: List[Command]):
        self.opt_tree = {c.name: c.argopts for c in commands}
        super().__init__()

    def get_style(self, selected: bool, flagged: bool = False):
        bg = self.STYLE_BG_FLAGGED if flagged else self.STYLE_BG_DEFAULT
        fg = self.STYLE_FG_SELECTED if selected else self.STYLE_FG
        return f"{bg} {fg}"

    def fuzzy_match(self, substring, options, position, title_func, uid_func = None, flag_func = lambda n: False):
        words = [w.lower() for w in substring.split(' ')]
        uid_func = title_func if uid_func is None else uid_func
        for option in sorted(options, key=lambda o: not flag_func(o)):
            display_title = title_func(option)
            match_title = display_title.lower()
            if all([w in match_title for w in words]):
                uid = uid_func(option)
                flagged = flag_func(option)
                style = self.get_style(False, flagged)
                selected_style = self.get_style(True, flagged)
                yield Completion(uid, -position, display_title, style=style, selected_style=selected_style)

    def get_subcompletions(self, subcmd, subopt, position):
        if subopt is None:
            return
        elif isinstance(subopt, dict):
            if ' ' in subcmd:
                k, v = subcmd.split(' ', 1)
                for completion in self.get_subcompletions(v, subopt.get(k), position - len(k) - 1):
                    yield completion
            else:
                for k in subopt.keys():
                    if k.startswith(subcmd):
                        yield Completion(k, -position, style=self.get_style(False), selected_style=self.get_style(True))
        elif isinstance(subopt, NoteFolder):
            if position == 0:
                subopt.pull()
            for completion in self.fuzzy_match(subcmd, [n for n in subopt.notes], position, lambda n: n.body.title, lambda n: n.uid, lambda n: n.flagged):
                yield completion

    def get_completions(self, document, complete_event):
        return self.get_subcompletions(document.text, self.opt_tree, document.cursor_position)


def with_args(*keys):
    def decorator(f):
        def wrapper(self, params):
            if len(keys) == 1:
                values = [params]
            else:
                values = params.split(' ', len(keys) - 1)
            return f(self, **{k: v for k, v in zip(keys, values)})
        return wrapper
    return decorator


def no_args(f):
    def wrapper(self, params):
        return f(self)
    return wrapper


class ApplicationREPL:

    def __init__(self, domain_name: str):
        self.notebox = Notebox(Config.from_yaml_file(os.path.join(os.getenv('HOME'), ".notebox", domain_name + ".yaml")))
        self.selected_note = None

        self.commands = [
            Command("zettel", self.select_zettel_command, self.notebox.zettels),
            Command("context",
                self.select_context_command,
                {
                    context_type_name: context_type
                    for context_type_name, context_type in self.notebox.context_types.items()
                }
            ),
            Command("deselect", self.deselect_command),
            Command("link", self.link_zettel_command, self.notebox.zettels),
            Command("edit", self.edit_note_command),
            Command("start", self.start_command),
            Command("stop", self.stop_command),
            Command("clean", self.clean_command),
            Command("quit", self.quit_command)
        ]

        self.completer = NoteCompleter(self.commands)
        self.session = PromptSession(completer=self.completer)

    def run(self):
        while True:
            try:
                input_text = self.session.prompt('> ', bottom_toolbar=self.toolbar)
                self.call_command(input_text)
            except (EOFError, KeyboardInterrupt):
                break
            except Exception as e:
                raise
                print(e)

    def call_command(self, input_text):
        if ' ' in input_text:
            command, params = input_text.split(' ', 1)
        else:
            command, params = input_text, None
        for c in self.commands:
            if command == c.name:
                c.func(params)
                return
        else:
            print(f"Unknown command {command}")

    def toolbar(self):
        if self.selected_note is None:
            note_type_indicator = ' '
        elif self.selected_note.note_type == NoteType.ZETTEL:
            note_type_indicator = 'Z'
        elif self.selected_note.note_type == NoteType.CONTEXT:
            note_type_indicator = 'C'
        else:
            note_type_indicator = ' '

        return f"[{self.notebox.name.upper()}] [{note_type_indicator}] {self.selected_note.body.title if self.selected_note is not None else '-'}"

    @with_args("uid")
    def link_zettel_command(self, uid):
        self.notebox.link(self.selected_note, self.notebox.zettels.notes_by_id[uid])

    def select_note(self, note_folder, uid_or_title):
        try:
            self.selected_note = note_folder.notes_by_id[uid_or_title]
        except KeyError:
            self.selected_note = note_folder.create(uid_or_title)

    @with_args("uid_or_title")
    def select_zettel_command(self, uid_or_title):
        self.select_note(self.zettels, uid_or_title)

    @with_args("context_type_name", "uid_or_title")
    def select_context_command(self, context_type_name, uid_or_title):
        self.select_note(self.notebox.context_types[context_type_name], uid_or_title)

    @no_args
    def start_command(self):
        if self.selected_note is None or self.selected_note.note_type != NoteType.CONTEXT:
            print('please select a context first')
            return
        self.notebox.edit_note(self.selected_note)
        cmd = ["timew", "start", self.notebox.name]
        if self.selected_note.provider_item.item_type == ContextProviderItemType.EVENT:
            cmd.append("meeting")
        else: 
            cmd.extend(self.selected_note.provider_item.attributes.get('tags', []))
        subprocess.Popen(cmd)
        subprocess.Popen(["timew", "annotate", self.selected_note.provider_item.title])

    @no_args
    def stop_command(self):
        subprocess.Popen(["timew", "stop"])

    @no_args
    def deselect_command(self):
        self.selected_note = None

    @no_args
    def edit_note_command(self):
        self.notebox.edit_note(self.selected_note)

    @no_args
    def clean_command(self):
        self.notebox.clean()

    @no_args
    def quit_command(self):
        self.notebox.clean()
        exit()


def main():
    ApplicationREPL(sys.argv[1]).run()

