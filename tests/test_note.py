#!/usr/bin/env

import pytest

from notebox.note import NoteBody, Link


note = NoteBody(
    title="Note Title",
    extra_attributes=dict(author="Some Guy"),
    content="Hello World!",
    links=[Link("Link 1", "./98765.md"), Link("Link 2", "./00000.md")],
    references=[Link("Reference 1", "../reference/type/ref1.md")]
)

markdown = """---
title: Note Title
author: Some Guy
---

Hello World!

---

**Links**

- [Link 1](./98765.md)
- [Link 2](./00000.md)

**References**

- [Reference 1](../reference/type/ref1.md)"""

note_ref_only = NoteBody(
    title="Note Title",
    content="Hello World!",
    references=[Link("Reference 1", "../reference/type/ref1.md")]
)

markdown_ref_only = """---
title: Note Title
---

Hello World!

---

**References**

- [Reference 1](../reference/type/ref1.md)"""

note_no_footer = NoteBody(
    title="Note Title",
    content="Hello World!",
)

markdown_no_footer = """---
title: Note Title
---

Hello World!"""

test_pairs = [
    (markdown, note),
    (markdown_ref_only, note_ref_only),
    (markdown_no_footer, note_no_footer)
]

@pytest.mark.parametrize("markdown,note", test_pairs)
def test_md_to_note(markdown,note):
    assert NoteBody.from_string(markdown) == note
    

@pytest.mark.parametrize("markdown,note", test_pairs)
def test_note_to_md(markdown,note):
    assert NoteBody.to_string(note) == markdown
    
