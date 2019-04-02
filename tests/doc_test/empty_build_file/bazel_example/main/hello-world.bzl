"""
An *example* .bzl file.

You will find here a rule, a macro and the implementation function for the rule.
"""


def custom_macro(name, format, srcs=[]):
    '''Custom macro documentation example.
    Args:

    :param format: The format to write check report in.
    :param srcs: Source files to run the checks against.

    '''
    pass


def __impl_custom_build_rule(ctx):
    """Documentation of the custom_build_rule implementation."""

    filesd = None
    return [DefaultInfo(files=filesd)]


custom_build_rule = rule(
    implementation = __impl_custom_build_rule,
    doc = """Explanation of **custom_build_rule**. Taken from `doc` attribute of rule definition.
""",
    attrs = {
        "targets": attr.label(
            mandatory=True,
            allow_files=True,
            doc="List of dependency rules which are building libraries"),
        "package_name": attr.string(
            mandatory=True,
            doc="Test string"),
        "package_script": attr.label(
            mandatory=False,
            default="//scripts:doc_gen_logger.py",
            allow_single_file=True,
            doc="Python script for simple file packaging"),
    }
)
