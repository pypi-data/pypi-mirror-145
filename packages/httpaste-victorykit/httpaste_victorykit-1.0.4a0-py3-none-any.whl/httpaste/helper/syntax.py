from pygments.lexers import get_lexer_by_name, find_lexer_class_by_name
from pygments.formatters import find_formatter_class, HtmlFormatter


def highlight(
        data: str,
        lexer_alias: str,
        format_alias: str,
        linenos: bool = False):

    from pygments import highlight

    if format_alias == 'html':

        formatter = HtmlFormatter(noclasses=True, linenos=linenos)
    else:

        formatter = find_formatter_class(format_alias)(linenos=linenos)

    return highlight(data, get_lexer_by_name(lexer_alias), formatter)
