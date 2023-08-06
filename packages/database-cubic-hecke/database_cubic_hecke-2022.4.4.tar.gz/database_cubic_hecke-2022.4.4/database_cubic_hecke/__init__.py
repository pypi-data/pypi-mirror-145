# -*- coding: utf-8 -*-
r"""
Utility to access data from `Ivan Marin's <http://www.lamfa.u-picardie.fr/marin/anglais.html>`__
web-page of `H4 representations  <http://www.lamfa.u-picardie.fr/marin/representationH4-en.html>`__
as Python functions in side `SageMath <https://www.sagemath.org/>`__.

Many thanks to Ivan Marin for making this data available.
"""

##############################################################################
#       Copyright (C) 2022 Sebastian Oehms <seb.oehms@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
##############################################################################

import os, enum
from database_cubic_hecke.marin_basis import _read_bas
from database_cubic_hecke.marin_irred_reprs import _read_irr
from database_cubic_hecke.marin_regl_reprs import _read_regl
from database_cubic_hecke.marin_regr_reprs import _read_regr

# -----------------------------------------------------------------------------
# globals
# -----------------------------------------------------------------------------

def version():
    r"""
    Return the current version of the databases.

    EXAMPLES::

        >>> from database_cubic_hecke import version
        >>> version() > '2022.1.3'
        True
    """
    from database_cubic_hecke import __version__
    return __version__.value


marin_url = 'http://www.lamfa.u-picardie.fr/marin/softs/H4/'
sympy_import_failure="""
This functionality requires SymPy (https://de.wikipedia.org/wiki/SymPy).
To install it type: pip install sympy.
"""

_cache = {}

class FileNames(enum.Enum):
    r"""
    Enum for constants which are shared with ``create_marin_data.py``.
    """
    def maple(self):
        r"""
        Return the Maple version for this filename.
        """
        return self.value[0]

    def py(self):
        r"""
        Return the Python version for this filename.
        """
        return self.value[1]

    def cache(self):
        r"""
        Return the cache key for this filename.
        """
        return self.value[2]

    basis             = ['baseH4.maple',             'marin_basis.py',       'bas']
    regular_left      = ['MatricesRegH4.maple',      'marin_regl_reprs.py',  'regl']
    regular_right     = ['MatricesRegH4right.maple', 'marin_regr_reprs.py',  'regr']
    irred_split       = ['RepresentationsH25',       'marin_irred_reprs.py', 'irr']
    markov_coeffs_irr = ['',                   'markov_trace_coeffs_irr.py', 'markov_irr']
    markov_coeffs     = ['',                   'markov_trace_coeffs.py',     'markov']


# -----------------------------------------------------------------------------
# protected functions
# -----------------------------------------------------------------------------

def _check_num_strands(num_strands):
    r"""
    Raise an error if the input is not allowed.

    EXAMPLES::

        >>> from database_cubic_hecke import _check_num_strands
        >>> _check_num_strands(5)
        Traceback (most recent call last):
        ...
        ValueError: num_strands must be less than 5
        >>> _check_num_strands(0)
        Traceback (most recent call last):
        ...
        ValueError: num_strands must be greater than 0
        >>> _check_num_strands('0')
        Traceback (most recent call last):
        ...
        TypeError: num_strands must be an integer
    """
    if not type(num_strands) is int:
        raise TypeError('num_strands must be an integer')
    if num_strands < 1:
        raise ValueError('num_strands must be greater than 0')
    if num_strands > 4:
        raise ValueError('num_strands must be less than 5')


def _mat_from_dict(dimension, dictionary):
    r"""
    Return a square matrix of the given dimension and entries
    according to the given dictionary.
    """
    from sympy import Matrix
    M = Matrix.zeros(dimension)
    for k, v in dictionary.items():
        M[k] = v
    return M

def _red_strands(name, cache_dict4, num_strands):
    r"""
    Reduce the data which belongs to the cubic Hecke algebra on 4 strands
    to the cubic Hecke algebra on ``num_strands`` strands.

    EXAMPLES::

        >>> from database_cubic_hecke import read_irr, _red_strands, FileNames
        >>> data4 = read_irr()
        >>> dim_list, repr_list, repr_list_inv = _red_strands(FileNames.irred_split, data4, 3)
        >>> dim_list
        [1, 1, 1, 2, 2, 2, 3]
        >>> repr_list[6][0]
        {(0, 0): c, (1, 0): a*c + b**2, (1, 1): b, (2, 0): b, (2, 1): 1, (2, 2): a}
        >>> data4 = read_reg()
        >>> dim_list, repr_list, repr_list_inv = _red_strands(FileNames.regular_right, data4, 2)
        >>> repr_list[0]
        [{(0, 1): -v, (0, 2): 1, (1, 0): 1, (1, 1): u, (2, 1): w}]
    """
    def red_gens(mlist):
        """
        Reduce the number of generators in the list of matrices.
        """
        return [mlist[i] for i in range(num_strands-1)]

    dim_list4, repr_list4, repr_list_inv4 = cache_dict4
    if name == FileNames.irred_split:
        max_ind = {1: 1, 2:3, 3:7}
        ind = range(max_ind[num_strands])
        dim_list = [dim_list4[i] for i in ind]
        repr_list = [red_gens(repr_list4[i]) for i in ind]
        repr_list_inv = [red_gens(repr_list_inv4[i]) for i in ind]
    else:
        bas4 = read_basis()
        bas  = read_basis(num_strands=num_strands)
        dim = len(bas)
        dim_list = [dim]
        rg = range(dim)
        ind = {k:bas4.index(bas[k]) for k in rg}
        def new_dict(mdict):
            pairs = [(i,j) for i in rg for j in rg if (ind[i], ind[j]) in mdict.keys()]
            return {(i,j):mdict[(ind[i], ind[j])] for (i,j) in pairs}
        def new_list(md_list):
            return [new_dict(md) for md in red_gens(md_list)]
        repr_list = [new_list(repr_list4[0])]
        repr_list_inv = [new_list(repr_list_inv4[0])]
    return dim_list, repr_list, repr_list_inv



def _read_repr(fname, variables, num_strands=4):
    r"""
    Return the data of the representations.

    EXAMPLES::

        >>> from database_cubic_hecke import _read_repr, FileNames
        >>> fname = FileNames.irred_split
        >>> from math import sqrt
        >>> j = (sqrt(3)*1j-1)/2
        >>> dim_list, repr_list, repr_list_inv = _read_repr(fname, (5, 7, 3, j))
        >>> dim_list
        [1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 6, 6, 6, 6, 6, 6, 8, 8, 8, 9, 9]
        >>> repr_list[5][1]
        {(0, 0): 3, (0, 1): -1, (1, 1): 5}
    """
    _check_num_strands(num_strands)
    cache_key = fname.cache()
    cache = None
    vtup = variables
    if cache_key in _cache.keys():
        cache = _cache[cache_key]
        if vtup in cache.keys():
            cache_dict =  cache[vtup]
            if num_strands in cache_dict.keys():
                return cache_dict[num_strands]
            if 4 in cache_dict.keys():
                cache_dict4 = cache_dict[4]
                red = _red_strands(fname, cache_dict4, num_strands)
                cache_dict[num_strands] = red
                return red
    if fname == FileNames.irred_split:
        dim_list, repr_list, repr_list_inv = _read_irr(*variables)
    elif fname == FileNames.regular_left:
        dim_list, repr_list, repr_list_inv = _read_regl(*variables)
    else:
        dim_list, repr_list, repr_list_inv = _read_regr(*variables)
    res = (dim_list, repr_list, repr_list_inv)
    if cache:
        section = {4: res}
        cache[vtup] = section
    else:
        section = {vtup: {4: res}}
        _cache[cache_key] = section
    if num_strands == 4:
        return res

    # recursion must work since cache has been changed
    return _read_repr(fname, variables, num_strands=num_strands)

# -----------------------------------------------------------------------------
# public functions
# -----------------------------------------------------------------------------

def read_basis(num_strands=4):
    r"""
    EXAMPLES::

        >>> from database_cubic_hecke import read_basis
        >>> b4 = read_basis()
        >>> len(b4)
        648
        >>> b2 = read_basis(num_strands=2); b2
        [[], [1], [-1]]
        >>> b3 = read_basis(num_strands=3)
        >>> len(b3)
        24
    """
    _check_num_strands(num_strands)
    if num_strands == 4:
        return _read_bas()
    else:
        basis_up = read_basis(num_strands=num_strands+1)
        return [b for b in basis_up if not num_strands in b and not -num_strands in b]

def read_irr(variables=None, num_strands=4):
    r"""
    Return the data of the irreducible split representations.

    EXAMPLES::

        >>> from database_cubic_hecke import read_irr
        >>> dim_list, repr_list, repr_list_inv = read_irr()
        >>> dim_list
        [1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 6, 6, 6, 6, 6, 6, 8, 8, 8, 9, 9]
        >>> repr_list[5][1]
        {(0, 0): c, (0, 1): -1, (1, 1): a}
        >>> from math import sqrt
        >>> j = (sqrt(3)*1j-1)/2
        >>> dim_list, repr_list, repr_list_inv = read_irr((5, 7, 3, j))
        >>> repr_list[23][0][(3, 8)]
        (1.5+6.06217782649107j)
    """
    if variables is None:
        try:
            from sympy import var, I, sqrt
        except ImportError:
            raise ImportError(sympy_import_failure)
        a, b, c = var('a, b, c')
        j = (sqrt(3)*I-1)/2
        variables = (a, b, c, j)
    return _read_repr(FileNames.irred_split, variables, num_strands=num_strands)

def read_reg(variables=None, right=False, num_strands=4):
    r"""
    Return the data of the regular representations.

    EXAMPLES::

        >>> from database_cubic_hecke import read_reg
        >>> dim_list, repr_list, repr_list_inv = read_reg()
        >>> dim_list
        [648]
        >>> [len(m) for m in repr_list[0]]
        [1080, 1701, 7862]
        >>> [len(m) for m in repr_list_inv[0]]
        [1080, 1728, 9370]
        >>> dim_list, repr_list, repr_list_inv = read_reg(num_strands=3)
        >>> dim_list
        [24]
        >>> [len(m) for m in repr_list[0]]
        [40, 63]
    """
    if variables is None:
        try:
            from sympy import var
        except ImportError:
            raise ImportError(sympy_import_failure)
        variables = var('u, v, w')
    if right:
         fname = FileNames.regular_right
    else:
         fname = FileNames.regular_left
    return _read_repr(fname, variables, num_strands=num_strands)

def irr_reprs_matrices(index, inverse=False, num_strands=4):
    r"""
    Return irreducible representation matrices of the cubic Hecke
    algebra for the given index.

    EXAMPLES::

        >>> from database_cubic_hecke import irr_reprs_matrices
        >>> m1, m2, m3 = irr_reprs_matrices(5)
        >>> m1i, m2i, m3i = irr_reprs_matrices(5, inverse=True)
        >>> m1 * m1i
        Matrix([
        [1, 0],
        [0, 1]])
        >>> m1*m2*m1 == m2*m1*m2
        True
        >>> m1i*m2i*m1i == m2i*m1i*m2i
        True
    """
    dim_list, repr_list, repr_list_inv = read_irr(num_strands=num_strands)
    l = len(repr_list)

    if not type(index) is int:
        raise TypeError('index must be of type int')
    if not index in range(l):
        raise ValueError('index must be in range(%s)' %l)

    if inverse:
        res_list = repr_list_inv[index]
    else:
        res_list = repr_list[index]
    dim = dim_list[index]

    return [_mat_from_dict(dim, d) for d in res_list]

def reg_reprs_matrices(right=False, inverse=False, num_strands=4):
    r"""
    Return the regular representation matrices of the cubic Hecke
    algebra for the given index and side.

    EXAMPLES::

        >>> from database_cubic_hecke import reg_reprs_matrices
        >>> m1, m2, m3 = reg_reprs_matrices()
        >>> m1.shape
        (648, 648)
        >>> m1i, m2i = reg_reprs_matrices(inverse=True, num_strands=3)
        >>> m1i.shape
        (24, 24)
        >>> m1i*m2i*m1i == m2i*m1i*m2i
        True
    """
    dim_list, repr_list, repr_list_inv = read_reg(right=right, num_strands=num_strands)

    if inverse:
        res_list = repr_list_inv[0]
    else:
        res_list = repr_list[0]
    dim = dim_list[0]

    return [_mat_from_dict(dim, d) for d in res_list]
