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
![alt text](./static/image.png)

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
  - frontmatter-url:
      button-text: 'My external button'
      frontmatter-url-name: 'github'
```

`button-text` is the text that is shown on the button.
The default is `Visit link`.

`frontmatter-url-name` is the name of the url-field in your frontmatter.
The default is `url`.

## Limitations

- The css is not configurable
- There are multiple fontawesome-icons usable as an icon, but the icon itself is not configurable
- There is only room for one URL
- The button will always try to place itself under the first heading. If there is no first heading it will place itself on the top

The interaction with other plugins has not been tested

## License

This project is licensed under the MIT License.
