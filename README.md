# Notebox

Notebox is a personal project to manage my notes and relate them to todo lists, calendars and timesheets.

## Model

### Note

A note corresponds to a single markdown file on disk.

Each note has 3 sections:

- Front Matter: metadata, being the title, and potentially extra attributes
- Content: the body of the note
- Footer: containing links to other notes

Only the content should be edited in the Editor. The application manages the Front Matter and Footer, so these should not be modified manually.

Notes all reside in a single flat directory, A unique identifier is used as filename, which is either based on the current timestamp, or the ID of the task or event that it relates to. 

### Zettel

A Zettel is a note which contains an atomic and autonomous idea. 

- Atomic: only a single idea is represented in the note
- Autonomous: the note explains the entire idea on its own

A Zettel's Front Matter will only contain a title. 

Its Footer will contain two types of links:

1. Links: links to other Zettels
2. References: links to Context Notes

The Content should not contain any links

### Context Note

A Context Note is a note which contains ideas and thoughts as they come up while in a specific Context. Such a Context can be in a meeting, while working on a project, or while working through a video course or book.

### Context Type

Examples of Context Types are:

- Projects: a short term objective about which thoughts and discoveries are logged
- Source: a video, book, article, etc. that is being studied and summarized
- Event: a meeting or call during which notes are taken

Each Context Type can be linked to a Context Provider.

### Context Provider

A Context Provider is a service where items of a certain Context Type are planned and tracked. Within a Context Provider, a Collection, being whatever that particular Context Provider sees as a list of items, is associated with a certain Context Type.

Currently implemented Context Providers are

- Todoist (`todoist`). Collection = Todoist Project
- Google Calendar (`gcal`). Collection = Calendar

## Configuration

A configuration for a single notebox is placed in a YAML configuration file

```yaml
name: mynotes
path: /home/user/notes
editor: vim # command for opening notes
context_providers:
  - name: mytodoist
    type: todoist
    params:
      apikey: "1234cdef"
  - name: mygcal
    type: gcal
    params:
      username: "john.smith@gmail.com"
      credentials_json_path: "/home/user/credentials.json"
context_types:
  - name: project
    title_format: "{created_time:%Y-%m-%d} - {title}"
    context_provider: 
      name: mytodoist
      collection: projectlist
  - name: source
    title_format: "{start_time:%Y-%m-%d %H:%M}-{end_time:%H:%M} - {title}"
    context_provider: 
      name: mytodoist
      collection: booklist
  - name: event
    context_provider: 
      name: mygcal
      collection: "john.smith@gmail.com"
    
```

## Installation

`cd` into the cloned repo folder and run

```bash
pip install .
```

## Usage

### REPL

Once your configuration is placed under `~/.notebox/<config>.yaml`, start the REPL with `notebox <config>`

### CLI

To be developed

## Design

I've chosen for certain simplifications over the traditional Zettelkasten:

- A Link is bidirectional. No distinction between Links and Backlinks
- No Tags, only Notes

I also prefer the idea behind the original Zettelkasten, where Links are made at the level of the full Note. This is where I'd differentiate Zettelkasten from a Wiki, where the word "apple" in the note body might get a link to more information about apples, even if apples aren't really central to the idea of the note.

Regarding Context Providers, the assumption is made that e.g. all projects are in a project list, a la GTD. This setup is currently not designed for where a list per project is made as needed.
