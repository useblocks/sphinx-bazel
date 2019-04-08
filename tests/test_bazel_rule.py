try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/bazel_rule')  # , warningiserror=True)
def test_bazel_rule(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert '//my/package:file.bzl:my_rule' in html
    assert 'my_rule'

