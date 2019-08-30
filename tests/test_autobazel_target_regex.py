try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/autobazel_target_regex')  # , warningiserror=True)
def test_autobazel_target_regex(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert 'hello-greet.cc' in html
    assert 'hello-greet.h' not in html
    assert 'hello-world.cc' in html
