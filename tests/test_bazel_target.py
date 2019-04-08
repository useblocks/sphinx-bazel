try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/bazel_target')  # , warningiserror=True)
def test_bazel_target(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert '//my/package:target' in html
    assert 'This target is a really nice looking one' in html

