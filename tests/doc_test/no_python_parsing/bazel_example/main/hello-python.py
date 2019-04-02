"""
PYTHON TEST: Should not be part of sphinx-bazel output
"""


def custom_macro(name, format, srcs=[]):
    """
    PYTHON TEST: Should not be part of sphinx-bazel output
    """
    pass


def __impl_custom_build_rule(ctx):
    """
    PYTHON TEST: Should not be part of sphinx-bazel output
    """
    filesd = None
    return [DefaultInfo(files=filesd)]


custom_build_rule = rule(
    implementation=__impl_custom_build_rule,
    doc="""
          PYTHON TEST: Should not be part of sphinx-bazel output
          """,
    attrs={
        "targets": attr.label(
            mandatory=True,
            allow_files=True,
            doc="PYTHON TEST: Should not be part of sphinx-bazel output"),
        "package_name": attr.string(
            mandatory=True,
            doc="PYTHON TEST: Should not be part of sphinx-bazel output"),
        "package_script": attr.label(
            mandatory=False,
            default="//scripts:doc_gen_logger.py",
            allow_single_file=True,
            doc="PYTHON TEST: Should not be part of sphinx-bazel output"),
    }
)
