from typing import List, Union

from pylatex import Alignat, NoEscape, LongTable, MultiColumn
from pytexit import py2tex


def py2tex_modified(exps: Union[List, str]):

    if isinstance(exps, tuple):
        exps = list(exps)

    if isinstance(exps, list):
        for i in range(len(exps)):
            try:
                exps[i] = f"${py2tex(f'{exps[i]}', print_latex=False, print_formula=False).replace('$', '')}$"
            except:
                pass
    elif isinstance(exps, str):
        try:
            exps = f"${py2tex(f'{exps}', print_latex=False, print_formula=False).replace('$', '')}$"
        except:
            pass
    else:
        raise TypeError('`exps` not list or str')
    return exps


def make_alginat_equations(latex_expressions: List[str], alignment_symbol: str = '='):
    alignat = Alignat(numbering=False, escape=False)
    for i, latex_expression in enumerate(latex_expressions):
        if i < len(latex_expressions) - 1:
            latex_expression += '\\\\'

        alignment_symbol_i = latex_expression.find(alignment_symbol)
        if alignment_symbol_i >= 0:
            latex_expression = f'{latex_expression[:alignment_symbol_i]}&{latex_expression[alignment_symbol_i:]}'

        alignat.append(latex_expression)

    return alignat


def make_table_of_symbols(symbols: List[str], units: List[str], descriptions: List[str]):
    table_symbols_content = LongTable("l l l")
    table_symbols_content.add_hline()
    table_symbols_content.add_row(["Symbol", "Unit", "Description"])
    table_symbols_content.add_hline()
    table_symbols_content.end_table_header()
    table_symbols_content.add_hline()
    table_symbols_content.add_row((MultiColumn(3, align='r', data='Continued on Next Page'),))
    table_symbols_content.add_hline()
    table_symbols_content.end_table_footer()
    table_symbols_content.add_hline()
    table_symbols_content.add_row((MultiColumn(3, align='r', data='***End'),))
    table_symbols_content.add_hline()
    table_symbols_content.end_table_last_footer()

    for i in range(len(symbols)):
        try:
            symbol = py2tex(symbols[i], print_latex=False, print_formula=False).replace('$', '')
        except:
            symbol = symbols[i]
        try:
            unit = py2tex(units[i], print_latex=False, print_formula=False, simplify_fractions=True).replace('$', '')
        except:
            unit = units[i]
        table_symbols_content.add_row([NoEscape(f'${symbol}$'), NoEscape(f'${unit}$'), NoEscape(descriptions[i])])

    table_symbols_content.add_hline()

    return table_symbols_content


def make_table(n_cols: int, headers: List, *args):
    table = LongTable(' '.join('l' * n_cols))
    table.add_hline()
    table.add_row(headers)
    table.add_hline()
    table.end_table_header()
    table.add_hline()
    table.add_row((MultiColumn(n_cols, align='r', data='Continued on Next Page'),))
    table.add_hline()
    table.end_table_footer()
    # table.add_hline()
    # table.add_row((MultiColumn(n_cols, align='r', data=''),))
    # table.add_hline()
    table.end_table_last_footer()

    for i in range(len(args[0])):
        table.add_row([NoEscape(j[i]) for j in args])

    table.add_hline()

    return table
