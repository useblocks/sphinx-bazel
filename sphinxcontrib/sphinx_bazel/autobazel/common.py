"""
autobazel-workspace
===================

"""
import ast

from docutils.parsers.rst import Directive, directives

import os
from pkg_resources import parse_version
import sphinx

sphinx_version = sphinx.__version__
if parse_version(sphinx_version) >= parse_version("1.6"):
    from sphinx.util import logging
else:
    import logging
logger = logging.getLogger(__name__)


class AutobazelCommonDirective(Directive):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        'packages': directives.flag,  # Shall packages inside a workspace be printed?
        'targets': directives.flag,  # Shall targets inside packages be printed?
        'rules': directives.flag,  # Shall rules inside bzl-files be printed?
        'macros': directives.flag,  # Shall macros inside bzl-files be printed?
        'implementations': directives.flag,  # Shall implementations inside bzl-files be printed?

        'hide': directives.flag,  # Shall the root-object be printed (e.g. no workspace)
        'workspace': directives.flag,  # Prints workspace name to all documented elements
        'workspace_path': directives.flag,  # Prints workspace_path name to all documented elements
        'implementation': directives.flag,  # Prints the used function name for implementation of a rule
    }
    final_argument_whitespace = True

    def __init__(self, *args, **kw):
        super(AutobazelCommonDirective, self).__init__(*args, **kw)
        self.log = logging.getLogger(__name__)

    @property
    def env(self):
        return self.state.document.settings.env

    @property
    def docname(self):
        return self.state.document.settings.env.docname

    def run(self):

        if 'workspace' not in self.name:

            try:
                self.workspace_name = self.env.ref_context['bazel:workspace']
            except KeyError:
                self.log.error("No workspace was defined before this package definition.\n "
                               "Please define one, which can than be used as reference for "
                               "calculating file paths.")
                return []

            try:
                self.workspace_path = self.env.domaindata['bazel']['workspaces'][self.workspace_name][1]
            except KeyError:
                self.log.error("Could not find workspace_name in defined workspace. That's strange!")
                return []
        else:
            self.workspace_path = self.arguments[0]

        if not os.path.isabs(self.workspace_path):
            self.workspace_path_abs = os.path.join(self.env.app.confdir, self.workspace_path)
        else:
            self.workspace_path_abs = self.workspace_path

        if not os.path.exists(self.workspace_path_abs):
            self.log.error("Given workspace does not exist: {}".format(self.arguments[0]))
            return []

        if 'workspace' in self.name:
            return self._handle_workspace()
        elif 'package' in self.name:
            return self._handle_package()
        elif 'target' in self.name:
            return self._handle_target()
        elif 'rule' in self.name:
            return self._handle_rule()

        return []

    def _handle_workspace(self):
        workspace_path = self.arguments[0]

        workspace_file_path = os.path.join(self.workspace_path_abs, 'WORKSPACE')
        if not os.path.exists(workspace_file_path):
            self.log.error("Given workspace path contains no WORKSPACE file.")
            return []

        with open(workspace_file_path) as f:
            tree = ast.parse(f.read(), workspace_file_path)
            workfile_docstring = ast.get_docstring(tree)
            try:
                for element in tree.body:
                    if isinstance(element.value, ast.Call) and element.value.func.id == 'workspace':
                        for keyword in element.value.keywords:
                            if keyword.arg == 'name':
                                workspace_name = keyword.value.s
                                break
            except KeyError:
                workspace_name = ""

            if not workspace_name:
                workspace_name = os.path.basename(os.path.normpath(workspace_path))
        if workfile_docstring is None:
            workfile_docstring = ""

        if self.options.get('hide', False) is None:  # If hide is set, no workpackage output
            workspace_rst = ""
        else:
            workspace_rst = """
.. bazel:workspace:: {workspace_name}
   :path: {path}

   {docstring}
            """.format(workspace_name=workspace_name,
                       path=workspace_path,
                       docstring="\n   ".join(workfile_docstring.split('\n')))

        if self.options.get('packages', False) is None:
            # Find packages inside workspace
            for root, dirs, files in os.walk(self.workspace_path_abs):
                if "BUILD" in files:
                    package = root.replace(self.workspace_path_abs, "")
                    package = "/" + package.replace("\\", "/")

                    workspace_rst += """
.. autobazel-package:: {package}""".format(package=package)
                    if self.options.get("workspace", False) is None:
                        workspace_rst += "\n   :workspace:"
                    if self.options.get("workspace_path", False) is None:
                        workspace_rst += "\n   :workspace_path:"
                    if self.options.get("targets", False) is None:
                        workspace_rst += "\n   :targets:"
                    if self.options.get("rules", False) is None:
                        workspace_rst += "\n   :rules:"
                    if self.options.get("implementation", False) is None:
                        workspace_rst += "\n   :implementation:"

        self.state_machine.insert_input(workspace_rst.split('\n'),
                                        self.state_machine.document.attributes['source'])
        return []

    def _handle_package(self):
        package = self.arguments[0]

        package_path = os.path.join(self.workspace_path_abs, package.replace('//', ''))
        package_build_file = os.path.join(package_path, 'BUILD')
        if not os.path.exists(package_build_file):
            self.log.error("No BUILD file detected for calculated package path: {}".format(package_path))
            return []

        with open(package_build_file) as f:
            tree = ast.parse(f.read(), package_build_file)
            package_docstring = ast.get_docstring(tree)
        if package_docstring is None:
            package_docstring = ""

        if self.options.get('hide', False) is None:  # If hide is set, no package output
            package_rst = ""
        else:
            options_rst = ""
            if self.options.get("workspace", False) is None:
                options_rst += "   :workspace:\n"
            if self.options.get("workspace_path", False) is None:
                options_rst += "   :workspace_path:\n"

            package_rst = """
.. bazel:package:: {package}
{options}

   {docstring}
            """.format(package=package,
                       options=options_rst,
                       docstring="\n   ".join(package_docstring.split('\n')))

        # Add target information
        if self.options.get('targets', False) is None:
            for root, dirs, files in os.walk(package_path):
                for package_file in files:
                    if package_file not in ['BUILD']:
                        target_signature = "{package}:{target_path}".format(
                            package=package,
                            target_path=os.path.join(root.replace(package_path, ''), package_file)
                        )
                        package_rst += "\n.. autobazel-target:: {target}".format(target=target_signature)
                        if self.options.get("workspace", False) is None:
                            package_rst += "\n   :workspace:"
                        if self.options.get("workspace_path", False) is None:
                            package_rst += "\n   :workspace_path:"
                        if self.options.get("rules", False) is None:
                            package_rst += "\n   :rules:"
                        if self.options.get("implementation", False) is None:
                            package_rst += "\n   :implementation:"

        self.state_machine.insert_input(package_rst.split('\n'),
                                        self.state_machine.document.attributes['source'])
        return []

    def _handle_target(self):
        target = self.arguments[0]

        target_path = os.path.join(self.workspace_path_abs, target.replace('//', '').replace(':', '/'))

        if not os.path.exists(target_path):
            self.log.error("Target does not exist: {target_path}".format(target_path=target_path))
            return []

        file_path, file_extension = os.path.splitext(target_path)
        if file_extension in ['.py', '.bzl']:  # Only check for docstring, if we are sure AST can handle it.
            with open(target_path) as f:
                try:
                    tree = ast.parse(f.read(), target_path)
                    target_docstring = ast.get_docstring(tree)
                except SyntaxError:
                    # Looks like file has no Python based syntax. So no documentation to catch
                    target_docstring = ""
        else:
            target_docstring = ""

        if target_docstring is None:
            target_docstring = ""

        options_rst = ""
        if self.options.get("workspace", False) is None:
            options_rst += "   :workspace:\n"
        if self.options.get("workspace_path", False) is None:
            options_rst += "   :workspace_path:\n"

        target_rst = """
.. bazel:target:: {target}
{options}
   {docstring}
        """.format(target=target,
                   options=options_rst,
                   docstring="\n   ".join(target_docstring.split('\n')))

        # Add rule information
        if self.options.get('rules', False) is None and file_extension in ['.bzl']:
            # Check for rules
            with open(target_path) as f:
                rule_names = []
                try:
                    tree = ast.parse(f.read(), target_path)
                    for element in tree.body:
                        # Check if we have something like rule_name = rule(...)
                        # where left part is the target and right part is the value
                        if isinstance(element, ast.Assign)\
                                and isinstance(element.value, ast.Call)\
                                and element.value.func.id == 'rule':
                            rule_names.append(element.targets[0].id)

                except SyntaxError:
                    self.log.error('Could not parse target: '.format(target_path))
                    return []

            for rule_name in rule_names:
                rule_signature = "{target}:{rule}".format(
                    target=target,
                    rule=rule_name)
                target_rst += "\n.. autobazel-rule:: {rule}".format(rule=rule_signature)
                if self.options.get("workspace", False) is None:
                    target_rst += "\n   :workspace:"
                if self.options.get("workspace_path", False) is None:
                    target_rst += "\n   :workspace_path:"
                if self.options.get("implementation", False) is None:
                    target_rst += "\n   :implementation:"

        self.state_machine.insert_input(target_rst.split('\n'),
                                        self.state_machine.document.attributes['source'])
        return []

    def _handle_rule(self):
        rule = self.arguments[0]
        rule_name = rule.rsplit(':', 1)[1]

        rule_file_path = os.path.join(self.workspace_path_abs,
                                      rule.replace('//', '').rsplit(":", 1)[0].replace(':', '/'))

        if not os.path.exists(rule_file_path):
            self.log.error("Target for rule does not exist: {rule_file_path}".format(target_path=rule_file_path))
            return []

        file_path, file_extension = os.path.splitext(rule_file_path)
        rule_doc = ""
        rule_impl = ""
        if file_extension in ['.bzl']:  # Only check for docstring, if we are sure AST can handle it.
            with open(rule_file_path) as f:
                try:
                    tree = ast.parse(f.read(), rule_file_path)
                    for element in tree.body:
                        # Check if we have something like rule_name = rule(...)
                        # where left part is the target and right part is the value
                        if isinstance(element, ast.Assign) and element.targets[0].id == rule_name and \
                                isinstance(element.value, ast.Call) and element.value.func.id == 'rule':
                            for keyword in element.value.keywords:
                                if keyword.arg == 'doc':
                                    rule_doc = keyword.value.s
                                if keyword.arg == 'implementation':
                                    rule_impl = keyword.value.id
                except SyntaxError:
                    # Looks like file has no Python based syntax. So no documentation to catch
                    rule_doc = ""

        # We have have found a rule_doc in the tree, but no value/None was set.
        if rule_doc is None:
            rule_doc = ""

        options_rst = ""
        if self.options.get("workspace", False) is None:
            options_rst += "   :workspace:\n"
        if self.options.get("workspace_path", False) is None:
            options_rst += "   :workspace_path:\n"
        if self.options.get("implementation", False) is None:
            options_rst += "   :implementation: {impl}\n".format(impl=rule_impl)

        rule_rst = """
.. bazel:rule:: {rule}
{options}
   {docstring}
        """.format(rule=rule,
                   options=options_rst,
                   docstring="\n   ".join(rule_doc.split('\n')))

        self.state_machine.insert_input(rule_rst.split('\n'),
                                        self.state_machine.document.attributes['source'])

        return []
