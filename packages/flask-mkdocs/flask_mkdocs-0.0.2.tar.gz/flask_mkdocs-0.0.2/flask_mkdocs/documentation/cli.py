"""
This module provides access to all the CLI commands for the app.
It is only meant to be used for generating documentation for the application's
command-line-interface with the 'mkdocs-click' plugin. 
"""
from pydoc import doc
from flask_mkdocs import documentation

cli = documentation.cli