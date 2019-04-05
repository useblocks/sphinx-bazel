try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/autobazel_implementation_options')  # , warningiserror=True)
def test_autobazel_options_path(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert 'main' in html
    assert 'workspace path' in html

