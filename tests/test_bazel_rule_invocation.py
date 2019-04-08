try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/bazel_rule_invocation')  # , warningiserror=True)
def test_bazel_rule_invocation(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert '//my/package:target:rule' in html
    assert 'invocation: rule(attribute_1, attribute_2)' in html


