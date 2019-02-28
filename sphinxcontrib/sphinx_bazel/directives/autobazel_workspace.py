"""
autobazel-workspace
===================

"""
import ast

from docutils.parsers.rst import Directive, nodes


import os
from pkg_resources import parse_version
import sphinx


sphinx_version = sphinx.__version__
if parse_version(sphinx_version) >= parse_version("1.6"):
    from sphinx.util import logging
else:
    import logging
logger = logging.getLogger(__name__)


class AutobazelWorkspaceDirective(Directive):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    option_spec = {}
    final_argument_whitespace = True
    
    def __init__(self, *args, **kw):
        super(AutobazelWorkspaceDirective, self).__init__(*args, **kw)
        self.log = logging.getLogger(__name__)

    @property
    def env(self):
        return self.state.document.settings.env

    @property
    def docname(self):
        return self.state.document.settings.env.docname
    
    def run(self):
        env = self.env
        
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
        
        workspace_rst = """
.. bazel:workspace:: AWESOME_NAME
   :path: {path}
   
   {docstring}
       """.format(path=workspace_path, docstring="\n   ".join(workfile_docstring.split('\n')))
        for root, dirs, files in os.walk(workspace_path_abs):
            if "BUILD" in files:
                package = root.replace(workspace_path_abs, "")
                package = "/" + package.replace("\\", "/")
                
                workspace_rst += """
.. bazel:package:: {package}
   :workspace:
   :workspace_path:
        """.format(package=package)

        contentnode = sphinx.addnodes.desc_content()
        # self.state.nested_parse(workspace_rst.split('\n'), self.content_offset, contentnode)
        self.state_machine.insert_input(workspace_rst.split('\n'),
                                        self.state_machine.document.attributes['source'])
        return []
