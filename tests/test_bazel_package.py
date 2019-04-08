try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/bazel_package')  # , warningiserror=True)
def test_bazel_package(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert '//my/package' in html
    assert 'Package content:' in html
    assert 'rule A' in html
    assert 'macro X' in html
    assert 'file 1'

