from pathlib import Path
from flask_mkdocs import documentation
import os
def test_init_docs(runner,tmp_path):
    Path(tmp_path)
    os.chdir(tmp_path)
    result = runner('docs init')
    docs_path = Path(tmp_path / 'docs')
    mkdocs_yml = docs_path / 'mkdocs.yml'
    assert mkdocs_yml.exists()

    assert documentation.INIT_SUCCESS_MESSAGE.format(docs_path.relative_to(tmp_path)) in result.output

    src_dir = mkdocs_yml.parent / 'src'
    assert src_dir.exists()

def test_build_docs(runner,tmp_path):
    os.chdir(tmp_path)
    result = runner('docs init')
    result = runner('docs build')
    yml = Path(tmp_path / 'docs' / 'mkdocs.yml')

    assert documentation.BUILD_SUCCESS_MESSAGE.format(yml.relative_to(tmp_path)) in result.output