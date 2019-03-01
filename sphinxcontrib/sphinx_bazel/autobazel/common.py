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
        'hide': directives.flag,  # Shall the root-object be printed (e.g. no workspace)
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
        
        if 'workspace' in self.name:
            return self._handle_workspace()
        elif 'package' in self.name:
            return self._handle_package()
        
        return []
    
    def _handle_workspace(self):
        workspace_path = self.arguments[0]
        if not os.path.isabs(workspace_path):
            workspace_path_abs = os.path.join(self.env.app.confdir, workspace_path)
        else:
            workspace_path_abs = workspace_path
        
        if not os.path.exists(workspace_path_abs):
            self.log.error("Given workspace does not exist: {}".format(self.arguments[0]))
            return []
        
        workspace_file_path = os.path.join(workspace_path_abs, 'WORKSPACE')
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
            for root, dirs, files in os.walk(workspace_path_abs):
                if "BUILD" in files:
                    package = root.replace(workspace_path_abs, "")
                    package = "/" + package.replace("\\", "/")
                    
                    workspace_rst += """
.. autobazel-package:: {package}
                    """.format(package=package)

        # Let the package-directive also know that targets shall get documented
        if self.options.get('targets', False) is None:
            workspace_rst += '   :targets:'
        
        self.state_machine.insert_input(workspace_rst.split('\n'),
                                        self.state_machine.document.attributes['source'])
        return []
    
    def _handle_package(self):
        package = self.arguments[0]
        
        try:
            workspace_name = self.env.ref_context['bazel:workspace']
        except KeyError:
            self.log.error("No workspace was defined before this package definition.\n "
                           "Please define one, which can than be used as reference for "
                           "calculating file paths.")
            return []
        
        try:
            workspace_path = self.env.domaindata['bazel']['workspaces'][workspace_name][1]
        except KeyError:
            self.log.error("Could not find workspace_name in defined workspace. That's strange!")
            return []
        
        if not os.path.isabs(workspace_path):
            workspace_path_abs = os.path.join(self.env.app.confdir, workspace_path)
        else:
            workspace_path_abs = workspace_path
        
        if not os.path.exists(workspace_path_abs):
            self.log.error("Given workspace does not exist: {}".format(self.arguments[0]))
            return []
        
        package_build_file = os.path.join(workspace_path_abs, package.replace('//', ''), 'BUILD')
        if not os.path.exists(package_build_file):
            self.log.error("No BUILD file detected for calculated package path: {}".format(package_build_file))
            return []
        
        with open(package_build_file) as f:
            tree = ast.parse(f.read(), package_build_file)
            package_docstring = ast.get_docstring(tree)
        if package_docstring is None:
            package_docstring = ""
        
        if self.options.get('hide', False) is None:  # If hide is set, no package output
            package_rst = ""
        else:
            package_rst = """
.. bazel:package:: {package}
   :workspace:

   {docstring}
            """.format(package=package, docstring="\n   ".join(package_docstring.split('\n')))
        
        # ToDo: autobazel-target for each found target must be added to package_rst
        
        self.state_machine.insert_input(package_rst.split('\n'),
                                        self.state_machine.document.attributes['source'])
        return []
