# Notebox

Notebox is a personal project to manage my notes and relate them to todo lists, calendars and timesheets. It's very oppinionated and built for my use case, so might need some work to fit someone else's needs.

## Model

### Note

A note corresponds to a single markdown file on disk.

Each note has 3 sections:

- Front Matter: metadata, being the title, and potentially extra attributes
- Content: the body of the note
- Footer: containing links to other notes

Only the content should be edited in the Editor. The application manages the Front Matter and Footer, so these should not be modified manually.

Notes all reside in a single flat directory, A unique identifier is used as filename, which is either based on the current timestamp, or the ID of the task or event that it relates to. 

### Zettel Note

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

#### Daily Note

Every day you get a note with the UID 'YYYY-MM-DD' to write non-specific notes

#### Source Note

A Source Note relates to a study resource, like a book or a video.

#### Project Note

A Project Note relates to a project.

#### Event Note

An Event Note relates to a calendar event, or any time window. It contains what was said during a meeting, etc.

### Context Provider

A Context Provider is a service where items of a certain Context Type are planned and tracked. Within a Context Provider, a Collection, being whatever that particular Context Provider sees as a list of items, is associated with a certain Context Type.

Currently implemented Context Providers are

- Todoist (`todoist`). Collection = Todoist Project
- Google Calendar (`gcal`). Collection = Calendar

### Domain

A Domain is an area where knowledge is applied. This can be `personal` for personal projects, `acme` for work, etc. The idea being that each Domain will have its own collection and providers

Notes outside the Domains are generic knowledge, while notes within a Domain apply to that Domain specifically. So a generic note about Python outside of the domains, could be linked to Company Python Guidelines in the `acme` Domain.

Source and Daily Notes are always domainless, while Event and Project Notes are always part of a Domain. 

### Comparisons With Zettelkasten

I've chosen for certain simplifications over the traditional Zettelkasten:

- A Link is bidirectional. No distinction between Links and Backlinks
- No Tags, only Notes

I also prefer the idea behind the original Zettelkasten, where Links are made at the level of the full Note. This is where I'd differentiate Zettelkasten from a Wiki, where the word "apple" in the note body might get a link to more information about apples, even if apples aren't really central to the idea of the note.

Regarding Context Providers, the assumption is made that e.g. all projects are in a project list, a la GTD. This setup is currently not designed for where a list per project is made as needed.

## Folder Structure

A notes folder has a somewhat oppinionated folder structure

```
<path>/
	daily/
	source/
	zettel/
	<domain>/
		event/
		project/
		zettel/
```

## Configuration

A configuration for a single notebox is placed in a YAML configuration file `~/.notebox/config.yaml`

```yaml
path: /home/john/notes
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
      credentials_json_path: "/home/john/credentials.json"
source:
  provider: todoist
  filter:
    project: source_projects
domains:
  - name: personal
    event: null # Don't use a context provider
    project:
      provider: todoist
      title_format: "{created_time:%Y-%m-%d} - {title}"
      filter:
        project: personal_* # Wildcards can be used
        priority: [3, 4] # Lists can be used
  - name: acme
    event:
      provider: gcal
      title_format: "{start_time:%Y-%m-%d %H:%M}-{end_time:%H:%M} - {title}"
      filter:
        calendar: "john.smith@gmail.com"
    project:
      provider: todoist
      title_format: "{created_time:%Y-%m-%d} - {title}"
      filter:
        project: work_*
```

## Installation

`cd` into the cloned repo folder and run

```bash
pip install .
```

## Usage

### REPL

Once your configuration is placed under `~/.notebox/config.yaml`, start the REPL with `notebox <config>`

Generic commands

- Type `[<domain>] <context_type>` and then start typing the title. Autocompletion will replace the title with an existing note's UID. If the note doesn't exist, the typed title stays and a new note is created with that title. The note is then set as the selected note, as seen in the bottom toolbar

```
acme project My Project
source My Textbook
```

- `quit`: exit application

Commands that act on the currently selected note

- `edit`: open in the editor
- `start`: start timewarrior with tags related to the note, and open in the editor
- `stop`: stop timewarrior

### CLI

To be developed