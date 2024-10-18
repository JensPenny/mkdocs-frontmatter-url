import re
import logging
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

log = logging.getLogger(__name__)

class FrontmatterUrlPlugin(BasePlugin):
    config_scheme = (
        ('button_text', config_options.Type(str, default='Visit Link')),
    )

    def on_page_markdown(self, markdown, page, config, files):
        log.error(f"on_page_markdown triggered for page: {page.file.src_path}")
        log.info(f'Meta informaton:{page.meta}')
        url = page.meta['url']
        button_text = self.config['button_text']
        button_html = f'<a href="{url}" class="frontmatter-url-button" target="_blank">{button_text}</a>\n\n'
        
        # Insert the button HTML after the frontmatter
        markdown = button_html + markdown
        log.info(f"Markdown processed for page: {page.file.src_path}")
        return markdown
