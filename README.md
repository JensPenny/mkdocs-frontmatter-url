# MkDocs Frontmatter URL Plugin

This MkDocs plugin generates a button or tag from a URL specified in the frontmatter of a markdown document.

## Installation

Install the package with pip:

```bash
pip install mkdocs-frontmatter-url
```

## Usage

1. Activate the plugin in your `mkdocs.yml`:

```yaml
plugins:
  - frontmatter-url
```

2. In your markdown files, add a `url` field to the frontmatter:

```yaml
---
title: My Page
gitlab: https://example.com
---

# Welcome to My Page

Content goes here...
```

3. The plugin will automatically generate a button with the specified URL after the frontmatter.

4. To verify if the `on_page_markdown` function is triggering, run MkDocs with the verbose flag:

```bash
mkdocs build -v
```

or for serving:

```bash
mkdocs serve -v
```

This will display detailed logs, including messages from the plugin showing when the `on_page_markdown` function is triggered for each page.

## Configuration

You can customize the button text in your `mkdocs.yml`:

```yaml
plugins:
  - search
  - frontmatter-url:
      button_text: 'Custom Button Text'
```

## License

This project is licensed under the MIT License.
