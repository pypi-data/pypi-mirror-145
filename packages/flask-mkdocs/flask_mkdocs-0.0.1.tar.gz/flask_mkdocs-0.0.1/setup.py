from setuptools import find_packages, setup
import os


def get_version():
    HERE = os.path.dirname(__file__)
    with open(os.path.join(HERE, NAME, "__version__.py")) as f:
        return f.read().strip()


NAME = "flask_mkdocs"
VERSION = get_version()

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths

DEV_REQUIREMENTS = [
    "pytest", 
    "pre-commit",
]
REQUIREMENTS = [
    "flask",
    "mkdocs",
    "pymdown-extensions",
    "mkdocs-material",
    "mkdocstrings",
    "mkdocs-macros-plugin",
    "mkdocs-git-revision-date-plugin",
    "interrogate",
    "mkdocs-click",
    "mkdocs-include-markdown-plugin",
    "mkdocs-minify-plugin",
    "lightgallery",
    "mkdocs-diagrams",
    "mkdocs-exclude",
    "keepachangelog",
    "changelog-cli",
    "adr-viewer",
]

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    package_data={NAME: package_files(NAME)},
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    extras_require={
        "dev": DEV_REQUIREMENTS  
    },
    entry_points={
        'flask.commands': [
            'docs=flask_mkdocs.documentation:cli'
        ],
    },
)
