# Database Cubic Hecke Algebras

This repository contains data for the representations of the
*Cubic Hecke Algebra* calculated by [Ivan Marin](http://www.lamfa.u-picardie.fr/marin/representationH4-en.html).
The original data of Ivan Marin are published in a format which
can be read by [Maple](https://en.wikipedia.org/wiki/Maple_(software)).
The purpose of this repository is, to make them available in
a Python like style such that they can be easily installed into
[SageMath](https://en.wikipedia.org/wiki/SageMath) using `pip`.

This repository was created as a part of the [SageMath](https://www.sagemath.org/)
functionality for the cubic Hecke algebras (see Trac ticket
[#29717](https://trac.sagemath.org/ticket/29717))

In addition to Ivan Marin's data it contains coefficients for linear forms
on the cubic Hecke algebras on up to four strands satisfying the Markov
trace condition (see for example
[Louis Kauffman: Knots and Physics, sections 7.1 and 7.2](https://www.worldscientific.com/worldscibooks/10.1142/4256)).
This data has been precomputed with the SageMath functionality
introduced by the above mentioned ticket
(see [Python module create_markov_trace_data.py](create_markov_trace_data.py)).

## Usage

In Python, it can be used as follows:

```python
>>> from database_cubic_hecke import read_basis
>>> b4 = read_basis()
>>> len(b4)
648
>>> b2 = read_basis(num_strands=2); b2
[[], [1], [-1]]
>>> b3 = read_basis(num_strands=3)
>>> len(b3)
24

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

>>> from database_cubic_hecke.markov_trace_coeffs import read_markov
>>> read_markov('U2', (3,5,7,11), num_strands=3)
[0, 11, 0.09090909090909091, 11, 0.09090909090909091, 0, 0, 0, 0, -55, 11, 11,
 -4.714285714285714, -0.45454545454545453, 0.09090909090909091, 0, 0, 0, 0,
 0.09090909090909091, -0.03896103896103896, -0.45454545454545453, 0, 0]
```

If you have [SymPy](https://de.wikipedia.org/wiki/SymPy) installed you can obtain
representation matrices directly:

```python
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

>>> from database_cubic_hecke import reg_reprs_matrices
>>> m1, m2, m3 = reg_reprs_matrices()
>>> m1.shape
(648, 648)
>>> m1i, m2i = reg_reprs_matrices(inverse=True, num_strands=3)
>>> m1i.shape
(24, 24)
>>> m1i*m2i*m1i == m2i*m1i*m2i
True

>>> from database_cubic_hecke.markov_trace_coeffs import read_markov
>>> from sympy import var
>>> u, v, w, s = var('u, v, w, s')
>>> variables = (u, v, w, s)
>>> read_markov('U2', variables, num_strands=3)
[0, s, 1/s, s, 1/s, 0, 0, 0, 0, -s*v, s, s, -s*u/w, -v/s, 1/s,
0, 0, 0, 0, 1/s, -u/(s*w), -v/s, 0, 0]
```

The usage in Sage will be implicitely via the new class `CubicHeckeAlgebra` according to
the Trac ticket [#29717](https://trac.sagemath.org/ticket/29717). But anyway, it can also
be used indenpendently, for example:

```python
sage: from database_cubic_hecke import read_irr
sage: F = CyclotomicField(3)
sage: L.<a, b, c> = LaurentPolynomialRing(F)
sage: T = L.gens_dict_recursive()
sage: T['j'] = T['zeta3']
sage: T.pop('zeta3')
sage: irr = read_irr(tuple(T.values()))
sage: dim_list, repr_list, repr_list_inv= irr
sage: m1d, m2d , m3d = repr_list[23]
sage: d = dim_list[23]
sage: m1 = matrix(d, d, m1d)
sage: m2 = matrix(d, d, m2d)
sage: m3 = matrix(d, d, m3d)
sage: m1
[             c              0              0              0              0              0              0              0              0]
[     b^2 + a*c              b              0              0              0              0   (-zeta3)*b*c              0              0]
[             b              1              a              0              0              0              c              0              0]
[             0              0              0              a              0              0             -c (-zeta3 - 1)*c    a + zeta3*b]
[   zeta3*a - b              0              0              0              b              0              0              0              0]
[       zeta3*a              0              0              0              b              a              0              0              0]
[             0              0              0              0              0              0              c              0              0]
[             0              0              0              0              0              0              0              c              0]
[             0              0              0              0              0              0              0        zeta3*c              b]

sage: m1*m2*m1 == m2*m1*m2
True
sage: m3*m2*m3 == m2*m3*m2
True
sage: m3*m1 == m1*m3
True


sage: from database_cubic_hecke import read_reg
sage: R.<u, v, w> = ZZ[]
sage: B = R.localization(w)
sage: T = B.gens_dict_recursive()
sage: reg = read_reg(tuple(T.values()))
sage: dim_list, repr_list, repr_list_inv= reg
sage: m1d, m2d , m3d = repr_list[0]
sage: d = dim_list[0]
sage: m1 = matrix(d, d, m1d)
sage: m2 = matrix(d, d, m2d)
sage: m3 = matrix(d, d, m3d)
sage: m1
648 x 648 sparse matrix over Multivariate Polynomial Ring in u, v, w over Integer Ring localized at (w,) (use the '.str()' method to see the entries)

sage: m1*m2*m1 == m2*m1*m2
True
sage: m3*m2*m3 == m2*m3*m2
True
sage: m3*m1 == m1*m3
True
```



To build a new release, the files containing the data in Python syntax can be
 upgraded with the [create_marin_data script](create_marin_data.py). There is a
[workflow](https://github.com/soehms/database_cubic_hecke/blob/main/.github/workflows/check_version_changed.yml)
to run this script and build a new release if differences are detected. It can
be triggered manually.

## Installation

### Python

```bash
pip install database_cubic_hecke
```

or

```bash
pip install database_cubic_hecke==2022.3.5
```

if you want to install a former version.


### SageMath

After release of the above mentioned Trac ticket, the database can be installed in Sage by:

```bash
sage -i database_cubic_hecke
```

This will contain integration with the cubic Hecke algebra functionality of Sage.
Before, or to use it independent on the new Sage functionality the installation
works as follows:

```bash
sage -pip install database_cubic_hecke
```

or

```bash
sage -pip install database_cubic_hecke==2022.3.5
```

for a special version.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/soehms/database_cubic_hecke)


## Versioning

Version numbers are automatically generated on a manually triggered workflow
`Check version changed` if differences to the original databases are detected.
They follow the scheme

\<year\>.\<month\>.\<day\>

with respect to the date the workflow is triggered.

## Help

If you note a divergence between this repository and the original data in case
the current release is older than a month please create an issue about that.

## Credits

Many thanks to Ivan Marin to make his data available for their use in Sage.
