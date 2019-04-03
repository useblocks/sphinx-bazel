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


@with_app(buildername='html', srcdir='doc_test/working_without_workspace')  # , warningiserror=True)
def test_working_without_workspace(app, status, warning):
    output = str(check_output(["sphinx-build", "-a", "-E", "-b", "html", app.srcdir, app.outdir],
                              stderr=STDOUT, universal_newlines=True))

    app.build()
    html = Path(app.outdir, 'index.html').read_text()
    assert '//domain_package/main' in html
    assert './domain_package-bazel-example' in html
    assert 'domain_package_test_data' in html

    assert '//domain_target/main:target' in html
    assert './domain_target-bazel-example' in html
    assert 'domain_target_test_data' in html

    assert '//domain_rule/main:target:rule' in html
    assert './domain_rule-bazel-example' in html
    assert 'domain_rule_test_data' in html

    assert 'Given workspace does not exist' not in output
    assert 'No workspace was defined before the' not in output

    assert '//main' in html
    assert 'MAIN package:' in html

    assert '//main:hello-world.cc' in html
    assert '//main:hello-world.bzl' in html
    assert 'You will find here a rule' in html

    assert '//main:hello-world.bzl:custom_build_rule' in html
    assert 'Explanation of' in html


