try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/autobazel_macro')  # , warningiserror=True)
def test_autobazel_macro(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert 'hello_world_workspace' in html
    assert 'My workspace description' in html
    assert 'main:hello-world.bzl:custom_macro' in html
    assert 'Args' in html
    assert 'Param format' in html
    assert 'The format to write check report in' in html
    assert 'Param srcs' in html
    assert 'Source files to run the checks against.' in html

