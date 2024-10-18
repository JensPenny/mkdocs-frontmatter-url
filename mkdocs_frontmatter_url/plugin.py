import re
import logging
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

log = logging.getLogger(__name__)

class FrontmatterUrlPlugin(BasePlugin):
    config_scheme = (
        ('button-text', config_options.Type(str, default='Visit Link')),
        ('frontmatter-url-name', config_options.Type(str, default='url')),
    )

    def on_page_markdown(self, markdown, page, config, files):
        log.error(f"on_page_markdown triggered for page: {page.file.src_path}")
        log.info(f'Meta informaton:{page.meta}')
        url_selector = self.config['frontmatter-url-name']
        url = page.meta[f'{url_selector}']
        button_text = self.config['button-text']
        button_html = f'<a href="{url}" class="frontmatter-url-button" target="_blank">{button_text}</a>\n\n'
        
        # Insert the button HTML after the frontmatter
        markdown = button_html + markdown
        log.info(f"Markdown processed for page: {page.file.src_path}")
        return markdown
