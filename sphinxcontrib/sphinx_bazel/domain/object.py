import re

from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.directives import ObjectDescription


# REs for Bazel signatures
bzl_sig_re = re.compile(
    r'''^  \/\/([\w\/]*)     # package name
           (:([\w]*))?          # target name
           $                 # and nothing more
          ''', re.VERBOSE)


class BazelObject(ObjectDescription):
    """
    Description of a general bazel object
    """
    option_spec = {
        'noindex': directives.flag,
        'workspace': directives.unchanged,
        'annotation': directives.unchanged,
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
            raise ValueError
        package, after_package, target, = m.groups()

        signode['workspace'] = self.env.ref_context['bazel:workspace']
        nodetext = package + '(workspace: ' + signode['workspace'] + ')'
        signode += addnodes.desc_addname(nodetext, nodetext)
        return sig, sig