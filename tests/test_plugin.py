import logging
import os
import pytest
import tempfile

from mkdocs.config import Config, defaults
from mkdocs.structure.pages import Page
from mkdocs.structure.files import File
from src.mkdocs_frontmatter_url.plugin import FrontmatterUrlPlugin

log = logging.getLogger(__name__)

@pytest.fixture
def temp_directory():
    with tempfile.TemporaryDirectory() as temp_dir: 
        yield temp_dir

# @pytest.fixture
# def config(temp_directory):
#     conf = defaults.MkDocsConfig()
#     conf.load_dict({
#         "docs_dir": temp_directory,
#         "frontmatter-url-name": "url"
#     })
#     return conf

@pytest.fixture
def config(temp_directory):
    return {
        'docs_dir': temp_directory,
        'plugins': {
            'frontmatter-url': {
                'frontmatter-url-name': 'url',
            }
        }
    }

@pytest.fixture
def site_navigation():
    return []

@pytest.fixture
def page(temp_directory, config): 
    dir = os.path.join(temp_directory, "test")
    os.mkdir(dir)
    path = os.path.join(dir, "test.md")
    page = Page(title="Test Page",
                file = File(path, temp_directory, temp_directory, False),
                config=config)
    return page

# This fixture will run the plugin on_markdown converter that will do the actual plugin logic
@pytest.fixture
def do_on_markdown(config, site_navigation, page):
    def md(markdown): 
        with open(page.file.abs_src_path, 'w') as f:
            f.write(markdown)
            
        plugin = FrontmatterUrlPlugin()
        log.info(f'injected config: {config}')
        page.read_source(config)
        plugin.config = config['plugins']['frontmatter-url']
        return plugin.on_page_markdown(markdown, page, config, site_navigation)
    return md 

frontmatter_block = """
---
url: https://example.com
---
"""    

def test_convert_with_heading(do_on_markdown):
    markdown_to_test = """
        # This is the first heading
         
        This is a test text
        
        ## This is the second heading

        Second test text
        """
    assert do_on_markdown(frontmatter_block + markdown_to_test) == 'faulty-test'