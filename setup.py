from setuptools import setup, find_packages

setup(
    name='mkdocs-frontmatter-url',
    version='0.1.0',
    description='A MkDocs plugin that generates a button from a URL in the frontmatter',
    long_description='This plugin for MkDocs takes a URL from the frontmatter of a markdown document and generates a button with that URL.',
    keywords='mkdocs plugin frontmatter url',
    url='https://github.com/JensPenny/mkdocs-frontmatter-url',
    author='Jens Penny',
    author_email='jens.penny+pypi@gmail.com',
    license='MIT',
    install_requires=[
        'mkdocs',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'frontmatter-url = mkdocs_frontmatter_url.plugin:FrontmatterUrlPlugin',
        ]
    }
)
