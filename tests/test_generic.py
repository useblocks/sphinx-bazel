try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/generic_doc')  # , warningiserror=True)
def test_generic(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert 'TEST DOCUMENT' in html

