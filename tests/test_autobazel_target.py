try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/autobazel_target')  # , warningiserror=True)
def test_autobazel_target(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert 'hello_world_workspace' in html
    assert 'My workspace description' in html
    assert 'main:hello-world.bzl' in html
    assert 'You will find here a rule, a macro and the implementation function for the rule.' in html