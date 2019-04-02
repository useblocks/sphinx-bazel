try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/empty_workspace_file')  # , warningiserror=True)
def test_empty_workspace_file(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert 'main' in html
    assert 'lib' in html

