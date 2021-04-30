# Notebox



## Model

### Note

A note corresponds to a single markdown file on disk.

Each note has 3 sections:

- Front Matter: metadata, being the title, and whatever attributes depending on the specific Context Type related to the note
- Content: the body of the note
- Footer: containing links to other notes

Only the content should be edited in the Editor. The application manages the Front Matter and Footer, so these should not be modified manually.

Notes all reside in a single flat directory, and are named with a UID based on the created timestamp.

### Zettel

A Zettel is a note which contains an atomic and autonomous idea. 

- Atomic: only a single idea is represented in the note
- Autonomous: the note explains the entire idea on its own

A Zettel's Front Matter will only contain a title. 

Its Footer will contain two types of links:

1. Links: links to other Zettels
2. References: links to Reference Notes

The Content should not contain any links

### Reference Note

A Reference Note is a note which contains ideas and thoughts as they come up while in a specific Context. Such a Context can be in a meeting, while working on a project, or while working through a video course or book.

A Reference Note's Front Matter will contain:

- A title
- Specific attributes provided by the Context Tyep

### Context Type

Examples of Context Types are:

- Projects: a short term objective about which thoughts and discoveries are logged
- Source: a video, book, article, etc. that is being studied and summarized
- Event: a meeting or call during which notes are taken

Each Context Type can be linked to a Context Provider.

### Context

A Context would be an item of a particular Context Type, e.g. a specific meeting, project, book, ...

### Context Provider

A Context Provider is a service where items of a certain Context Type are planned and tracked. Within a Context Provider, a Collection, being whatever that particular Context Provider sees as a list of items, is associated with a certain Context Type.

Currently implemented Context Providers are

- Todoist (`todoist`). Collection = Todoist Project
- Google Calendar (`gcal`). Collection = Calendar

## Configuration

A configuration for a single notebox is placed in a YAML configuration file

```yaml
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
    context_provider: mytodoist
    collection: projectlist
  - name: source
    context_provider: mytodoist
    collection: booklist
    extra_attributes:
      - author
      - medium
      - link
  - name: event
    context_provider: mygcal
    collection: "john.smith@gmail.com"
    
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

I also prefer the idea behind the original Zettelkasten, where Links are made at the level of the full Note. Thisis where I'd differentiate Zettelkasten from a Wiki, where the word "apple" in the note body might get a link to more information about apples, but the central idea of the note not having much relationship to apples.

Regarding Context Providers, the assumption is made that e.g. all projects are in a project list, a la GTD. This setup is currently not designed for where a list per project is made as needed.

## Development

Code structure

```
notebox/
	
```