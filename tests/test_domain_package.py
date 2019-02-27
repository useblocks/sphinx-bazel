try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/domain_package_doc')  # , warningiserror=True)
def test_domain_package(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert 'BAZEL_PACKAGE_A' in html
    assert 'BAZEL_PACKAGE_A_CONTENT' in html

