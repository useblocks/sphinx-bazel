try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/autobazel_package_regex')  # , warningiserror=True)
def test_autobazel_package(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert 'MAIN package' in html
    assert 'LIB package' not in html



