try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/autobazel_implementation_options')  # , warningiserror=True)
def test_autobazel_implementation_options(app, status, warning):
    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert 'workspace-my custom workspace'
    assert 'My workspace description' in html
    assert 'lib' in html
    assert 'lib:hello-time.cc' in html
    assert 'lib:hello-time.h' in html
    assert 'main' in html
    assert 'main:hello-world.cc' in html
    assert 'main:hello-world.bzl' in html
    assert 'main:hello-greet.cc' in html
    assert 'main:hello-world.bzl:custom_build_rule' in html
    assert 'main:hello-world.bzl:custom_macro' in html
    assert 'main:hello-world.bzl:__impl_custom_build_rule' in html
    assert 'implementation: __impl_custom_build_rule' in html
    assert 'workspace: my custom workspace' in html
    assert 'workspace path: ./bazel_example' in html


