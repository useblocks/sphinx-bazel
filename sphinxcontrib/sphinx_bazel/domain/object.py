import re

from docutils.parsers.rst import directives, nodes

from pkg_resources import parse_version

import sphinx
from sphinx import addnodes
from sphinx.directives import ObjectDescription


sphinx_version = sphinx.__version__
if parse_version(sphinx_version) >= parse_version("1.6"):
    from sphinx.util import logging
else:
    import logging
logger = logging.getLogger(__name__)

# REs for Bazel signatures
bzl_sig_re = re.compile(
    r'''^  \/\/([\w\/]*)     # package name
           (:([\w\/.-]*))?   # target name
           (:([\w\/.-]*))?   # rule, macro or impl name (named later internally as internal)
           $                 # and nothing more
          ''', re.VERBOSE)


class BazelObject(ObjectDescription):
    """
    Description of a general bazel object
    """
    option_spec = {
        'workspace': directives.flag,
        'workspace_path': directives.flag,
        'implementation': directives.unchanged,  # Used by bazel:rule to print implementation function
    }

    def get_signature_prefix(self, sig):
        # type: (str) -> str
        """May return a prefix to put before the object name in the
        signature.
        """
        return ''

    def needs_arglist(self):
        # type: () -> bool
        """May return true if an empty argument list is to be generated even if
        the document contains none.
        """
        return False

    def handle_signature(self, sig, signode):
        """
        Transform a Bazel signatur into RST nodes.
        
        :param sig:
                :param signode:
        :return:
        """
        m = bzl_sig_re.match(sig)
        if m is None:
            logger.error("Sphinx-Bazel: Parse problems with signature: {}".format(sig))
            raise ValueError
        package, after_package, target, after_target, internal = m.groups()

        try:
            signode['workspace'] = self.env.ref_context['bazel:workspace']
        except KeyError:
            logger.error("No workspace defined before given Bazel element on current page.")
        
        signode['package'] = package
        signode['target'] = target
        
        sig_text = '//{}'.format(package)
        if target:
            sig_text += ':{}'.format(target)
        if internal:
            sig_text += ':{}'.format(internal)
        signode += addnodes.desc_name(sig_text, sig_text)
        
        if self.options.get('workspace', False) is None:  # if flag is set, value is None
            ws_string = 'workspace: {}'.format(signode['workspace'])
            self._add_signature_detail(signode, ws_string)
            
        if self.options.get('workspace_path', False) is None:  # if flag is set, value is None
            current_ws = self.env.ref_context['bazel:workspace']
            ws_obj = self.env.domaindata['bazel']['workspaces'][current_ws]
            ws_path = ws_obj[1]  # See workspace.py for details about stored data
            ws_path_string = 'workspace path: {}'.format(ws_path)
            self._add_signature_detail(signode, ws_path_string)

        rule_impl = self.options.get('implementation', "")
        if rule_impl:  # if flag is set, value is None
            impl_string = 'implementation: {}'.format(rule_impl)
            self._add_signature_detail(signode, impl_string)
        
        return sig, sig

    def _add_signature_detail(self, signode, text):
        """
        Create a additional line under signature.
        Used to show additional details of an object like workspace name or path
        
        :param signode: node to add the line add the ending
        :param text: Text inside the new line
        :return: None
        """
        ws_line = nodes.line()
        ws_line += addnodes.desc_addname(text, text)
        signode += ws_line
