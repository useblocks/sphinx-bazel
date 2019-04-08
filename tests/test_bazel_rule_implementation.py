try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/bazel_rule_implementation')  # , warningiserror=True)
def test_bazel_bazel_rule_implementation(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert 'workspace-workspace_rule_impl_example' in html
    assert 'implementation: __my_rule_func'
