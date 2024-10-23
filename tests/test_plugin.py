import logging
import os
import pytest
import tempfile
import re
import yaml

from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page
from mkdocs.structure.files import File
from mkdocs.plugins import PluginCollection
from src.mkdocs_frontmatter_url.plugin import FrontmatterUrlPlugin

log = logging.getLogger(__name__)

@pytest.fixture
def temp_directory():
    with tempfile.TemporaryDirectory() as temp_dir: 
        yield temp_dir

@pytest.fixture
def config(temp_directory):
    config = MkDocsConfig()
    config.load_dict({
        'docs_dir': temp_directory,
    })

    # We'll add the plugin and its config to the base config, and grab it from there in the tests
    frontmatter_url_plugin = FrontmatterUrlPlugin()
    frontmatter_url_plugin.load_config({
        'frontmatter-url-name': 'url',
        'button-text': 'Visit link'
    })
    config.plugins = PluginCollection([('frontmatter-url', frontmatter_url_plugin)])
    return config

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

@pytest.fixture
def do_on_markdown(config, site_navigation, page):
    def md(markdown): 
        # Parse frontmatter and populate the meta object
        parts = markdown.split('---', 2)
        if len(parts) == 3:
            fm, content = parts[1], parts[2]
            page.meta = yaml.safe_load(fm) # This took way too long
        else:
            content = markdown
            page.meta = {}
        
        # Write the markdown to the temp. page
        with open(page.file.abs_src_path, 'w') as f:
            f.write(markdown)
    
        plugin = config.plugins['frontmatter-url']
        log.info(f'Page meta: {page.meta}')
        return plugin.on_page_markdown(content.strip(), page, config, site_navigation)
    return md 

# Test: A normal markdown file with a first and second heading
# We expect the button to be under the first heading
def test_convert_with_base_heading(do_on_markdown):
    frontmatter_block = """
---
url: https://example.com
---
"""

    markdown_to_test = """
# This is the first heading

This is a test text

## This is the second heading

Second test text
"""
    result = do_on_markdown(frontmatter_block + markdown_to_test)
    log.info(result)

    assert_basic_style(result)

    # Check if the button is inserted after the first heading
    first_heading_pattern = r'# This is the first heading'
    button_pattern = r'<a href="https://example.com" class="frontmatter-url-tag" target="_blank">'
    assert re.search(f'{first_heading_pattern}.*?{button_pattern}', result, re.DOTALL) is not None

    # Check if the original content is preserved
    assert 'This is a test text' in result
    assert '## This is the second heading' in result
    assert 'Second test text' in result

# Test: A normal markdown file starting with a second heading
# We expect the button to be above the second heading
def test_convert_with_second_heading(do_on_markdown):
    frontmatter_block = """
---
url: https://example.com
---
"""

    markdown_to_test = """
## This is the second heading

Second test text
"""
    result = do_on_markdown(frontmatter_block + markdown_to_test)

    assert_basic_style(result)
        
    # Check if the button is inserted before the second heading. The first heading is the page title by default
    second_heading_pattern = r'## This is the second heading'
    button_pattern = r'<a href="https://example.com" class="frontmatter-url-tag" target="_blank">'
    assert re.search(f'{button_pattern}.*?{second_heading_pattern}', result, re.DOTALL) is not None

    # Check if the original content is preserved
    assert '## This is the second heading' in result
    assert 'Second test text' in result

# Test: A normal markdown file without a heading
# We expect the button to be above the markdown text
def test_convert_without_headings(do_on_markdown):
    frontmatter_block = """
---
url: https://example.com
---
"""

    markdown_to_test = """
This is just a basic text
Some stuff without headings is also possible
"""
    result = do_on_markdown(frontmatter_block + markdown_to_test)
    log.info(result)

    assert_basic_style(result)
        
    # Check if the button is the top of the document
    button_pattern = r'<a href="https://example.com" class="frontmatter-url-tag" target="_blank">'
    text_pattern = r'This is just a basic text'
    assert re.search(f'{button_pattern}.*?{text_pattern}', result, re.DOTALL) is not None

    # Check if the original content is preserved
    assert 'This is just a basic text' in result
    assert 'Some stuff without headings is also possible' in result

# Utility function to assert if the basic style and script elements are preserved in the generated markdown
def assert_basic_style(result):
    assert '<style>' in result
    assert '<script src="https://kit.fontawesome.com/e147252cfa.js" crossorigin="anonymous"></script>' in result
    assert '<a href="https://example.com" class="frontmatter-url-tag" target="_blank">' in result
    assert '<i class="fas fa-comment-alt"></i>Visit link</a>' in result
