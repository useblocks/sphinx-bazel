try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

try:
    from StringIO import StringIO  # Python 2
except ImportError:
    from io import StringIO  # Python 3
from subprocess import check_output, STDOUT

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/empty_workspace_file')  # , warningiserror=True)
def test_empty_workspace_file(app, status, warning):
    output = str(check_output(["sphinx-build", "-a", "-E", "-b", "html", app.srcdir, app.outdir],
                              stderr=STDOUT, universal_newlines=True))
    print(output)
    html = Path(app.outdir, 'index.html').read_text()
    assert 'main' in html
    assert 'lib' in html

