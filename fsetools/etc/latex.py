from operator import itemgetter
from typing import List, Union

from pylatex import Alignat, NoEscape, LongTable, MultiColumn

try:
    from pytexit import py2tex
except ModuleNotFoundError:
    pass


def py2tex_modified(exps: Union[List, tuple, str]):
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


def make_summary_table(symbols: list, units: dict, descriptions: dict, values: dict):
    def make_table(headers: List, *args):
        table = LongTable('|l| l| l| p{10cm}|')
        table.add_hline()
        table.add_row([NoEscape(f'\\textbf{{\\textcolor{{black}}{{{i}}}}}') for i in headers])
        table.add_hline()
        table.end_table_header()
        table.add_hline()
        table.add_row((MultiColumn(4, align='r', data='Continued on next page'),))
        # table.add_hline()
        table.end_table_footer()
        # table.add_hline()
        # table.add_row((MultiColumn(n_cols, align='r', data=''),))
        # table.add_hline()
        table.end_table_last_footer()

        for i in range(len(args[0])):
            table.add_row([NoEscape(j[i]) for j in args])
            table.add_hline()

        return table

    for i in list(set(symbols) - set(values)):
        symbols.remove(i)

    units = [units[symbol] for symbol in symbols]
    values = [values[symbol] for symbol in symbols]
    descriptions = [descriptions[symbol] for symbol in symbols]

    true_values = [i for i, v in enumerate(values) if isinstance(v, (float, int))]

    table = make_table(
        ['Symbol', 'Unit', 'Value', 'Description'],
        py2tex_modified(itemgetter(*true_values)(symbols)),
        py2tex_modified(itemgetter(*true_values)(units)),
        [f'{value:g}' for value in itemgetter(*true_values)(values)],
        [description[0].upper() + description[1:] for description in itemgetter(*true_values)(descriptions)],
    )
    return table
