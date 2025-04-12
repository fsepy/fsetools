from fsetools.etc.latex import *


def test_py2tex_modified():
    assert py2tex_modified(r'a = b ** 2 + c ** 2') == '$a=b^2+c^2$'
    assert py2tex_modified(r'E = m * c ** 2') == '$E=m c^2$'
    assert py2tex_modified([r'a = b ** 2 + c ** 2', r'E = m * c ** 2', ], ignore_error=False)


def test_make_alginat_equations():
    obj = make_alginat_equations(py2tex_modified([r'a = b ** 2 + c ** 2', r'E = m * c ** 2', ], ignore_error=False))
    assert obj.dumps() == '\\begin{alignat*}{2}%\n$a&=b^2+c^2$\\\\%\n$E&=m c^2$%\n\\end{alignat*}'


def test_make_table_of_symbols():
    obj = make_table_of_symbols(
        symbols=['\\rho_a', 'T_0', '\\lambda_\\theta'],
        units=['kg/m**3', 'K', '-'],
        descriptions=['Density of steel', 'Initial temperature', 'Reduction factor']
    )
    print(obj.dumps())


def test_make_summary_table():
    obj = make_summary_table(
        symbols=['rho_a', 'T_0', 'lambda_theta'],
        units={'rho_a': 'kg/m**3', 'T_0': 'K', 'lambda_theta': '-'},
        descriptions={'rho_a': 'Density of steel', 'T_0': 'Initial temperature', 'lambda_theta': 'Reduction factor'},
        values={'rho_a': 1, 'T_0': 2, 'lambda_theta': 3}
    )
    print(obj.dumps())


test_py2tex_modified()
test_make_alginat_equations()
test_make_table_of_symbols()
test_make_summary_table()
