try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/bazel_workspace')  # , warningiserror=True)
def test_bazel_workspace(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert 'workspace-my_workspace_name' in html
    assert 'workspace description' in html


