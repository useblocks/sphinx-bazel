from sphinx import version_info


def create_indexnode(indextext, fullname):
    # See https://github.com/sphinx-doc/sphinx/issues/2673
    if version_info < (1, 4):
        return ('single', indextext, fullname, '')
    else:
        return ('single', indextext, fullname, '', None)
