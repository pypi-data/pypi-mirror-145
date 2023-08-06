import argparse
import re


def doc_text(dealer):  # (...) -> str
    text = getattr(dealer, '__doc__', '')
    return text.strip() if text and text.strip() else dealer.__name__


def get_summary(func):
    return doc_text(func).splitlines()[0]


def show_help(func):
    print(doc_text(func))
    print()


def add_subcommand(name, func):
    parser_args = [name]
    parser_kwargs = {
        'help': get_summary(func),
        'description': doc_text(func),
        'formatter_class': argparse.RawDescriptionHelpFormatter
    }
    parser_item = parser_args, parser_kwargs, func

    def f(g):
        if not hasattr(g, '__argparse_parsers__'):
            setattr(g, '__argparse_parsers__', [])
        getattr(g, '__argparse_parsers__').insert(0, parser_item)
        return g
    return f


def add_argument(name, *, short='', type=None, default=None, help='', required=True, choices=None, nargs=None, dest=''):
    opt_args, opt_kwargs = [], {}
    assert re.match(r'(--)?\w+', name) is not None
    if short:
        assert re.match(r'\w', short) is not None
        if name.startswith('--'):
            opt_args.append('-' + short)
        else:
            opt_kwargs['metavar'] = short

    opt_args.append(name)
    if type == bool:
        opt_kwargs['action'] = 'store_true'
    elif type is not None:
        opt_kwargs['type'] = type
    if default is not None:
        opt_kwargs['default'] = default
    opt_kwargs['help'] = help
    if required and name.startswith('--'):
        opt_kwargs['required'] = True
    elif required is False and not name.startswith('--') and not nargs:
        opt_kwargs['nargs'] = '?'
    if choices is not None:
        assert isinstance(choices, list)
        opt_kwargs['choices'] = choices
    if nargs:  # https://docs.python.org/3/library/argparse.html#nargs
        opt_kwargs['nargs'] = nargs
    if dest:
        opt_kwargs['dest'] = dest
    opt_item = opt_args, opt_kwargs

    def f(g):
        if not hasattr(g, '__argparse_args__'):
            setattr(g, '__argparse_args__', [])
        getattr(g, '__argparse_args__').insert(0, opt_item)
        return g
    return f


def run(dealer):
    def bind(parser, func):
        if hasattr(func, '__argparse_parsers__'):
            parsers = parser.add_subparsers()
            for parser_args, parser_kwargs, sub_func in getattr(func, '__argparse_parsers__'):
                sub_parser = parsers.add_parser(*parser_args, **parser_kwargs)
                sub_parser.set_defaults(_func=sub_func)
                bind(sub_parser, sub_func)
        if hasattr(func, '__argparse_args__'):
            for opt_args, opt_kwargs in getattr(func, '__argparse_args__'):
                parser.add_argument(*opt_args, **opt_kwargs)
        parser.set_defaults(_func=func)
        parser.set_defaults(_parser=parser)

    root_parser = argparse.ArgumentParser(description=doc_text(dealer), formatter_class=argparse.RawDescriptionHelpFormatter)
    bind(root_parser, dealer)
    args = root_parser.parse_args()
    cur_parser = getattr(args, '_parser')
    cur_func = getattr(args, '_func')
    if hasattr(cur_func, '__argparse_args__') or not hasattr(cur_func, '__argparse_parsers__'):
        try:
            cur_func(**{k: v for k, v in args.__dict__.items() if k[0] != '_'})
        except AssertionError as e:
            if str(e):
                cur_parser.error(str(e) + '!\n')
            else:
                cur_parser.error('-h or --help for help!')
    else:
        cur_parser.print_help()


def main():
    text = """
    
    Boilerplate of Installable Project:
        git clone https://github.com/qorzj/lesscli.git

    Documentation of "Writing the Setup Script":
        https://docs.python.org/2/distutils/setupscript.html
        https://docs.python.org/3/distutils/setupscript.html
        
    Argparse Tutorial:
        https://docs.python.org/3/howto/argparse.html
        https://docs.python.org/3/library/argparse.html

    Documentation of lesscli.run:
        >>> import lesscli
        >>> help(lesscli.run)

    """
    print(text)
