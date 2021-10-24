## Principles:

- Documentation as Code (it's version managed and controlled, there is a 'live' version) 
- It should be obvious what the Engineer should do next, but require them to do very little that they wouldn't normally be doing.

## User Stories:

- Where do I read the documentation? - Documentation is made centrally available on a static site.
- Where do I write the documentation? - Documentation lives in the code (as docstrings) and in .md files in a docs folder.
- How do I update documentation? - Documentation is submitted along with code to the `main` branch.
- How do I fix a problem with the documentation? - Documentation lives in the source code repositories, submit a PR with the correction.

## Outline Design:

- A **docs/** folder is added to each repository - templates are provided in empty folders to give Engineers a starting point.
- Either triggered by the PR or on a schedule, **Docward** looks for docstrings in code and creates an automatic document file.
- If **Docward** finds a **docs/** folder, it reads well-known .md files in this folder (e.g. quickstart.md, design.md) and includes these alongside the documentation extracted from the code.
- Documentation is written in plain text (markdown/docstrings) with extensions for diagrams using something like [mermaid](https://mermaid-js.github.io/mermaid/#/) - **Docward** convers these .md files to HTML and creates a static site (with a search - something like [lunr](https://lunrjs.com/))
- Documentation is published on a static site with a site map something like:

~~~graphml
  ├── index.html
  ├── <repository_name>/
  │     ├── index.html
  │     ├── code.html
  │     └── design.html
  ├── <respository_name>/
  │     ├── index.html
  │     └── code.html
  etc
~~~

## Quality Indicators

- Quality Indicators - doc updates should have a cadence inline with the code
- Quality Indicators - doc size should be a ratio of the KLOC
- Quality Indicators - Links in documents respond with a 200 (immediately or following redirects) to an HTTP GET request

##
