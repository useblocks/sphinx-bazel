try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/autobazel_package')  # , warningiserror=True)
def test_autobazel_package(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert 'hello_world_workspace' in html
    assert 'My workspace description' in html
    assert 'lib' in html


@with_app(buildername='html', srcdir='doc_test/autobazel_package_multi')  # , warningiserror=True)
def test_autobazel_package_multiple(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert 'hello_world_workspace' in html
    assert 'My workspace description' in html
    assert 'main' in html
    assert '//main/sub' in html
    assert '//main/sub:hello-sub.cc' in html

