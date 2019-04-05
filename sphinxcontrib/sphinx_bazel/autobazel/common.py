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
        'attributes': directives.flag,  # Shall attributes of rule be printed?
        'path': directives.unchanged,  # Used as temporary workspace path, if given.
        'name': directives.unchanged,  # Used to manually set a name of a workspace

        'hide': directives.flag,  # Shall the root-object be printed (e.g. no workspace)
        'show_workspace': directives.flag,  # Prints workspace name to all documented elements
        'show_workspace_path': directives.flag,  # Prints workspace_path name to all documented elements
        'show_implementation': directives.flag,  # Prints the used function name for implementation of a rule
    }
    final_argument_whitespace = True

    def __init__(self, *args, **kw):
        super(AutobazelCommonDirective, self).__init__(*args, **kw)
        self.log = logging.getLogger(__name__)

        self.root_path = None
        self.workspace_name = None
        self.workspace_path = None
        self.workspace_path_abs = None

    @property
    def env(self):
        return self.state.document.settings.env

    @property
    def docname(self):
        return self.state.document.settings.env.docname

    def run(self):

        if 'workspace' not in self.name:
            self.root_path = self.options.get('path', False)
            if self.root_path:
                self.workspace_path = self.root_path
                self.workspace_name = os.path.basename(self.root_path)
            else:
                try:
                    self.workspace_name = self.env.ref_context['bazel:workspace']
                except KeyError:
                    self.log.error("No workspace was defined before the {} definition of {}.\n "
                                   "Please define one, which can than be used as reference for "
                                   "calculating file paths.\n"
                                   "Or use option :root-path: to document something without"
                                   "a bazel workspace.".format(self.name, self.arguments[0]))
                    return []

                try:
                    self.workspace_path = self.env.domaindata['bazel']['workspaces'][self.workspace_name][1]
                except KeyError:
                    self.log.error("Could not find workspace_name in defined workspace. That's strange!")
                    return []
        else:
            if self.options.get('path', False):
                self.log.warning(':path: not supported by autobazel-workspace. Argument is used instead.')
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
        elif 'macro' in self.name or 'implementation' in self.name:
            return self._handle_macro_implementation()
        elif 'attribute' in self.name:
            return self._handle_attribute()

        return []

    def _handle_workspace(self):
        workspace_path = self.arguments[0]

        workspace_file_path = os.path.join(self.workspace_path_abs, 'WORKSPACE')
        if not os.path.exists(workspace_file_path):
            self.log.error("Given workspace path contains no WORKSPACE file.")
            return []

        workspace_name = ""
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
                pass

            if not workspace_name:
                workspace_name = os.path.basename(os.path.normpath(workspace_path))

        #  Set a specific workspace name, if given
        if self.options.get('name', False):
            workspace_name = self.options.get('name', '')

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
                    if self.options.get('show_workspace', False) is None:
                        workspace_rst += "\n   :show_workspace:"
                    if self.options.get('show_workspace_path', False) is None:
                        workspace_rst += "\n   :show_workspace_path:"
                    if self.options.get("targets", False) is None:
                        workspace_rst += "\n   :targets:"
                    if self.options.get("rules", False) is None:
                        workspace_rst += "\n   :rules:"
                    if self.options.get("implementations", False) is None:
                        workspace_rst += "\n   :implementations:"
                    if self.options.get("macros", False) is None:
                        workspace_rst += "\n   :macros:"
                    if self.options.get("attributes", False) is None:
                        workspace_rst += "\n   :attributes:"
                    if self.options.get("show_implementation", False) is None:
                        workspace_rst += "\n   :show_implementation:"
                    if self.options.get("path", False):
                        workspace_rst += "\n   :path: {}".format(self.root_path)

        self.state_machine.insert_input(workspace_rst.split('\n'),
                                        self.state_machine.document.attributes['source'])
        return []

    def _handle_package(self):
        package = self.arguments[0]

        package_path = os.path.join(self.workspace_path_abs, package.replace('//', ''))
        package_build_file = os.path.join(package_path, 'BUILD')
        if not os.path.exists(package_build_file):
            self.log.error("No BUILD file detected for calculated package path: {} in file {}."
                           "Used workspace {} in {}".format(package, self.state.document.current_source,
                                                            self.workspace_name, self.workspace_path_abs))
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
            if self.options.get('show_workspace', False) is None:
                options_rst += "   :show_workspace:\n"
            if self.options.get('show_workspace_path', False) is None:
                options_rst += "   :show_workspace_path:\n"
            if self.options.get('path', False):
                options_rst += "   :path: {}\n".format(self.workspace_path_abs)

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
                        if self.options.get('show_workspace', False) is None:
                            package_rst += "\n   :show_workspace:"
                        if self.options.get('show_workspace_path', False) is None:
                            package_rst += "\n   :show_workspace_path:"
                        if self.options.get("rules", False) is None:
                            package_rst += "\n   :rules:"
                        if self.options.get("implementations", False) is None:
                            package_rst += "\n   :implementations:"
                        if self.options.get("macros", False) is None:
                            package_rst += "\n   :macros:"
                        if self.options.get("attributes", False) is None:
                            package_rst += "\n   :attributes:"
                        if self.options.get("show_implementation", False) is None:
                            package_rst += "\n   :show_implementation:"
                        if self.options.get("path", False):
                            package_rst += "\n   :path: {}".format(self.root_path)

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
        if file_extension in ['.bzl']:  # Only check for docstring, if we are sure AST can handle it.
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
        if self.options.get('hide', False) is None:  # If hide is set, no target output
            target_rst = ""
        else:
            if self.options.get('show_workspace', False) is None:
                options_rst += "   :show_workspace:\n"
            if self.options.get('show_workspace_path', False) is None:
                options_rst += "   :show_workspace_path:\n"
            if self.options.get('path', False):
                options_rst += "   :path: {}\n".format(self.workspace_path_abs)

            target_rst = """
.. bazel:target:: {target}
{options}
   {docstring}
            """.format(target=target,
                       options=options_rst,
                       docstring="\n   ".join(target_docstring.split('\n')))

        # Add rule, macro, implementation information
        if (self.options.get('rules', False) is None
            or self.options.get('macros', False) is None
            or self.options.get('implementations', False) is None) \
                and file_extension in ['.bzl']:
            # Check for rules, macros and implementations
            with open(target_path) as f:
                rule_names = []
                macro_names = []
                implementation_names = []
                try:
                    tree = ast.parse(f.read(), target_path)
                    for element in tree.body:
                        # Check if we have something like rule_name = rule(...)
                        # where left part is the target and right part is the value
                        if isinstance(element, ast.Assign) \
                                and isinstance(element.value, ast.Call) \
                                and element.value.func.id == 'rule':
                            rule_names.append(element.targets[0].id)
                        elif isinstance(element, ast.FunctionDef):
                            # rule_implementation get only 'ctx as argument. Nothing else.
                            if len(element.args.args) == 1 and element.args.args[0].arg == 'ctx':
                                implementation_names.append(element.name)
                            # if it does not get 'ctx' as argument, it must be a macro.
                            else:
                                macro_names.append(element.name)
                except SyntaxError:
                    self.log.error('Could not parse target: '.format(target_path))
                    return []

            if self.options.get('rules', False) is None:
                for rule_name in rule_names:
                    rule_signature = "{target}:{rule}".format(
                        target=target,
                        rule=rule_name)
                    target_rst += "\n.. autobazel-rule:: {rule}".format(rule=rule_signature)
                    target_rst += self._add_options()

            if self.options.get('macros', False) is None:
                for macro_name in macro_names:
                    macro_signature = "{target}:{macro}".format(
                        target=target,
                        macro=macro_name)
                    target_rst += "\n.. autobazel-macro:: {macro}".format(macro=macro_signature)
                    target_rst += self._add_options()

            if self.options.get('implementations', False) is None:
                for implementation_name in implementation_names:
                    implementation_signature = "{target}:{implementation}".format(
                        target=target,
                        implementation=implementation_name)
                    target_rst += "\n.. autobazel-implementation:: {implementation}".format(
                        implementation=implementation_signature)
                    target_rst += self._add_options()

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
        rule_attrs = []
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
                                if keyword.arg == 'attrs':
                                    rule_attrs = [x.s for x in keyword.value.keys]
                except SyntaxError:
                    # Looks like file has no Python based syntax. So no documentation to catch
                    rule_doc = ""

        # We have have found a rule_doc in the tree, but no value/None was set.
        if rule_doc is None:
            rule_doc = ""

        options_rst = ""
        options_rst += "   :implementation: {impl}\n".format(impl=rule_impl)
        if self.options.get('show_workspace', False) is None:
            options_rst += "   :show_workspace:\n"
        if self.options.get('show_workspace_path', False) is None:
            options_rst += "   :show_workspace_path:\n"
        if self.options.get("show_implementation", False) is None:
            options_rst += "   :show_implementation: \n"
        if self.options.get('path', False):
            options_rst += "   :path: {}\n".format(self.workspace_path_abs)

        rule_rst = """
.. bazel:rule:: {rule}
{options}
   {docstring}
        """.format(rule=rule,
                   options=options_rst,
                   docstring="\n   ".join(rule_doc.split('\n')))

        if self.options.get('attributes', False) is None:
            for attr_name in rule_attrs:
                attribute_signature = "{rule}:{attribute}".format(rule=rule, attribute=attr_name)
                rule_rst += "\n.. autobazel-attribute:: {attribute}".format(attribute=attribute_signature)
                rule_rst += self._add_options()

        self.state_machine.insert_input(rule_rst.split('\n'),
                                        self.state_machine.document.attributes['source'])

        return []

    def _handle_macro_implementation(self):
        macro = self.arguments[0]
        macro_name = macro.rsplit(':', 1)[1]

        macro_file_path = os.path.join(self.workspace_path_abs,
                                       macro.replace('//', '').rsplit(":", 1)[0].replace(':', '/'))

        if not os.path.exists(macro_file_path):
            self.log.error("Target for macro does not exist: {target_path}".format(target_path=macro_file_path))
            return []

        file_path, file_extension = os.path.splitext(macro_file_path)
        macro_doc = ""
        if file_extension in ['.bzl']:  # Only check for docstring, if we are sure AST can handle it.
            with open(macro_file_path) as f:
                try:
                    tree = ast.parse(f.read(), macro_file_path)
                    for element in tree.body:
                        if isinstance(element, ast.FunctionDef) and element.name == macro_name:
                            # ToDo: If we shall document an implementation, we should check if *ctx* is the only
                            # ToDo: argument
                            try:
                                macro_doc = element.body[0].value.s
                            except [KeyError, AttributeError, IndexError]:
                                macro_doc = ""
                except SyntaxError:
                    # Looks like file has no Python based syntax. So no documentation to catch
                    macro_doc = ""

        # We have have found a rule_doc in the tree, but no value/None was set.
        if macro_doc is None:
            macro_doc = ""

        options_rst = ""
        if self.options.get('show_workspace', False) is None:
            options_rst += "   :show_workspace:\n"
        if self.options.get('show_workspace_path', False) is None:
            options_rst += "   :show_workspace_path:\n"
        if self.options.get('path', False):
            options_rst += "   :path: {}\n".format(self.workspace_path_abs)

        macro_rst = """
.. bazel:macro:: {macro}
{options}
   {docstring}
        """.format(macro=macro,
                   options=options_rst,
                   docstring="\n   ".join(macro_doc.split('\n')))

        self.state_machine.insert_input(macro_rst.split('\n'),
                                        self.state_machine.document.attributes['source'])

        return []

    def _handle_attribute(self):
        """Cares about the correct handling of autobazel-attributes"""
        attribute_path = self.arguments[0]

        try:
            package_name, target_name, rule_name, attribute_name = attribute_path.rsplit(':', 3)
        except IndexError:
            self.log.warning("bazel-path for autobazel-attribute looks strange: {}".format(attribute_path))

        target_file_path = os.path.join(self.workspace_path_abs, package_name.replace('//', ''),
                                      target_name.replace(':', '/'))

        if not os.path.exists(target_file_path):
            self.log.error("Target for r ule does not exist: {target_path}".format(target_path=target_file_path))
            return []

        file_path, file_extension = os.path.splitext(target_file_path)
        rule_doc = ""
        rule_impl = ""
        rule_found = False
        attributes_found = False
        attributes = {}
        if file_extension in ['.bzl']:  # Only check for docstring, if we are sure AST can handle it.
            with open(target_file_path) as f:
                try:
                    tree = ast.parse(f.read(), target_file_path)
                    for element in tree.body:
                        # Check if we have something like rule_name = rule(...)
                        # where left part is the target and right part is the value
                        if isinstance(element, ast.Assign) and element.targets[0].id == rule_name and \
                                isinstance(element.value, ast.Call) and element.value.func.id == 'rule':
                            rule_found = True
                            for keyword in element.value.keywords:
                                if keyword.arg == 'doc':
                                    rule_doc = keyword.value.s
                                if keyword.arg == 'implementation':
                                    rule_impl = keyword.value.id
                                if keyword.arg == 'attrs':
                                    attributes_found = True
                                    for index, key in enumerate(keyword.value.keys):
                                        value = keyword.value.values[index]
                                        attributes[key.s] = {
                                            'type': value.func.attr,
                                            'parameters': {}
                                        }
                                        for param_keyword in value.keywords:
                                            if isinstance(param_keyword.value, ast.NameConstant):
                                                needed_value = str(param_keyword.value.value)
                                            elif isinstance(param_keyword.value, ast.Str):
                                                needed_value = param_keyword.value.s

                                            attributes[key.s]['parameters'][param_keyword.arg] = needed_value

                except (SyntaxError, KeyError) as e:
                    # Looks like file has no Python based syntax. So no documentation to catch
                    self.log.warning("Problems during parsing of {} happened: {}".format(target_file_path, e))
                    return []

        if not rule_found:
            self.log.warning('Rule {} not found for autobazel-attribute'.format(rule_name))
            return []

        if not attributes_found:
            self.log.warning('Attributes not found for rule {}'.format(rule_name))
            return []

        if attribute_name not in attributes.keys():
            self.log.warning('Attribute {} not found in rule {}. Available attributes: {}'.format(
                attribute_name, rule_name, ', '.join(attributes.keys())
            ))
            return []

        attribute = attributes[attribute_name]

        try:
            doc_string = attribute['parameters']['doc']
        except KeyError:
            doc_string = ''

        options_rst = ""
        options_rst += "   :implementation: {impl}\n".format(impl=rule_impl)
        if self.options.get('show_workspace', False) is None:
            options_rst += "   :show_workspace:\n"
        if self.options.get('show_workspace_path', False) is None:
            options_rst += "   :show_workspace_path:\n"
        if self.options.get('path', False):
            options_rst += "   :path: {}\n".format(self.workspace_path_abs)

        rule_rst = """
.. bazel:rule:: {path}
{options}
   {docstring}
        """.format(path=attribute_path,
                   options=options_rst,
                   docstring="\n   ".join(doc_string.split('\n')))

        self.state_machine.insert_input(rule_rst.split('\n'),
                                        self.state_machine.document.attributes['source'])

        return []

    def _add_options(self):
        """
        Adds needed options
        """
        directive_rst = ""
        if self.options.get('show_workspace', False) is None:
            directive_rst += "\n   :show_workspace:"
        if self.options.get('show_workspace_path', False) is None:
            directive_rst += "\n   :show_workspace_path:"
        if self.options.get("implementations", False) is None:
            directive_rst += "\n   :implementations:"
        if self.options.get("macros", False) is None:
            directive_rst += "\n   :macros:"
        if self.options.get("attributes", False) is None:
            directive_rst += "\n   :attributes:"
        if self.options.get("show_implementation", False) is None:
            directive_rst += "\n   :show_implementation:"
        if self.options.get("path", False):
            directive_rst += "\n   :path: {}".format(self.root_path)
        return directive_rst


