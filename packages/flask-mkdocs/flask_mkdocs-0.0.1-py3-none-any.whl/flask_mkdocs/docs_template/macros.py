import html
import os
from typing import List, Optional

DOCS_DIR = "src"
CODE_DIR = "../flask_theme_adminlte3/documentation"


def define_env(env):
    @env.macro
    def code_from_file(fn: str, flavor: str = "", pre=False):
        """
        Load code from a file and save as a preformatted code block.
        If a flavor is specified, it's passed in as a hint for syntax highlighters.

        Example usage in markdown:

            {{code_from_file("code/myfile.py", "python")}}

        """
        v = env
        # docs_dir = variables.get("docs_dir", DOCS_DIR)
        fn = os.path.abspath(os.path.join(CODE_DIR, fn))
        if not os.path.exists(fn):
            return f"""<b>File not found: {fn}</b>"""
        with open(fn, "r") as f:

            source = f.read()
            if pre:
                source = f"""<pre><code class="{flavor}">{html.escape(source)}</code></pre>"""

        return source

    @env.macro
    def render_changelog(filename: Optional[str] = None):
        """
        Load changelog markdown files relative to the reposity root
        Example usage in markdown:

            {{render_changelog("CHANGELOG.md")}}

        """

        if not filename:
            filename = env.variables.get("changelog", "CHANGELOG.md")

        # Load the changelog
        docs_dir = os.path.dirname(env.conf.get("docs_dir", DOCS_DIR))
        repo_dir = os.path.dirname(docs_dir)
        changelog_file = os.path.abspath(os.path.join(repo_dir, str(filename)))
        try:
            import keepachangelog

            changelog = keepachangelog.to_dict(
                changelog_path=changelog_file, show_unreleased=True
            )
        except:
            if not os.path.exists(changelog_file):
                return ''
            with open(changelog_file) as f:
                return f.read()

        # Load the Template
        from jinja2 import Template

        template_file = env.variables.get("changelog", "changelog.html.jinja2")
        templates_dir = os.path.join(docs_dir, "templates")
        template_file = os.path.abspath(os.path.join(templates_dir, template_file))
        with open(template_file) as file_:
            template = Template(file_.read())

        from dataclasses import dataclass

        @dataclass
        class Change:
            kind: str
            color: str
            text: str

        @dataclass
        class Release:
            version: str
            title: str
            caption: str
            changes: List[Change]

        """
        sample changelong json

        ```json
        "1.0.1": {
            "fixed": [
                "Bug fix 1 (1.0.1)",
                "sub bug 1",
                "sub bug 2",
                "Bug fix 2 (1.0.1)",
            ],
            "metadata": {
                "release_date": "2018-05-31",
                "version": "1.0.1",
                "semantic_version": {
                    "major": 1,
                    "minor": 0,
                    "patch": 1,
                    "prerelease": None,
                    "buildmetadata": None,
                },
                "url": "https://github.test_url/test_project/compare/v1.0.0...v1.0.1",
            },
        },
        ```
        """

        releases = []
        deprecations = []

        for (version, release_json) in changelog.items():
            metadata = release_json.get("metadata", {})
            date = metadata.get("release_date", release_json.get("release_date"))
            caption = "unreleased"
            if date:
                caption = f"released on {date}"

            changes = []
            for f in ["fix", "fixed", "fixes"]:
                changes += [
                    Change("Fixed", "fixed", text) for text in release_json.get(f, [])
                ]
            for f in ["change", "changed", "changes"]:
                changes += [
                    Change("Changed", "changed", text)
                    for text in release_json.get(f, [])
                ]
            for f in ["feat", "feature", "features", "added", "add", "adds", "new"]:
                changes += [
                    Change("Added", "added", text) for text in release_json.get(f, [])
                ]
            for f in ["deprecated", "deprecate"]:
                deprecated = [
                    Change("Deprecated", "deprecate", text)
                    for text in release_json.get(f, [])
                ]
                deprecations += deprecated
                changes += deprecated
            for f in ["remove", "removed", "delete", "deleted"]:
                changes += [
                    Change("Removed", "removed", text)
                    for text in release_json.get(f, [])
                ]
            for f in ["breaks", "break", "breaking"]:
                changes += [
                    Change("Breaking", "security", text)
                    for text in release_json.get(f, [])
                ]
            for f in ["security", "update"]:
                changes += [
                    Change("Security", "security", text)
                    for text in release_json.get(f, [])
                ]

            releases.append(Release(version, "", caption, changes))

        # Render the template
        rendered = template.module.render(releases=releases, deprecated=deprecations)

        return rendered

    @env.macro
    def external_markdown(fn: str):
        """
        Load markdown from files external to the mkdocs root path.
        Example usage in markdown:

            {{external_markdown("../../README.md")}}

        """
        docs_dir = env.conf.get("docs_dir", DOCS_DIR)
        fn = os.path.abspath(os.path.join(docs_dir, fn))
        if not os.path.exists(fn):
            return f"""<b>File not found: {fn}</b>"""
        with open(fn, "r") as f:
            return f.read()
