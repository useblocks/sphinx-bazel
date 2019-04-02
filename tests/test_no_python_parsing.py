try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/no_python_parsing')  # , warningiserror=True)
def test_no_python_parsing(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert 'main' in html
    assert 'lib' in html
    assert 'lib' in html
    assert 'hello-python.py' in html
    assert 'PYTHON TEST' not in html

