"""
In order to get at more extensions, I wanted to use
   https://pythonhosted.org/Markdown instead of
   https://github.com/trentm/python-markdown2

So I made this custom parser ala plim docs here:
   http://plim.readthedocs.org/en/latest/en/extensions.html

Extensions available are here:
   https://pythonhosted.org/Markdown/extensions/index.html

"""
import re
import plim

# markdown and my wanted extensions
import markdown
from markdown.extensions.smarty import SmartyExtension
from markdown.extensions.extra import ExtraExtension

FIND_MARKDOWN_RE = re.compile('-\s*(?P<lang>md|markdown)\s*')

def my_markdown(text):
    # configure the markdown the way I want it...
    return markdown.markdown(
        text, output_format='html5',
        extensions=[ SmartyExtension(), ExtraExtension() ]
    )

# ripped off from plim.lexer.parse_markup_languages...
def parse_markdown_custom(indent_level, current_line, matched, source, syntax):
    '''A plim parser that just uses my own opinionated markdown instead of
    its own...'''
    parsed_data, tail_indent, tail_line, source = plim.lexer.parse_explicit_literal_no_embedded(
        indent_level,
        '|',
        matched,
        source,
        syntax
        )
    parsed_data = my_markdown(parsed_data)
    return parsed_data.strip(), tail_indent, tail_line, source

CUSTOM_PLIM_PARSERS = [
    (FIND_MARKDOWN_RE, parse_markdown_custom)
]

plim_preprocessor = plim.preprocessor_factory(
    custom_parsers=CUSTOM_PLIM_PARSERS, syntax='mako')
