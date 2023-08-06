import sys
import optparse
from .util import eafp


def doc_text(dealer):  # (...) -> str
    text = getattr(dealer, '__doc__', '')
    return text.strip() if text and text.strip() else dealer.__name__


def show_help(dealer):
    print(doc_text(dealer))
    print()


def add_option(name, *, short='', long='', type='str', default=None, help=''):
    opt_args, opt_kwargs = [], {}
    if short:
        assert short[0] == '-' and len(short) == 2
        opt_args.append(short)
    assert name and name[0] != '-'
    opt_kwargs['dest'] = name
    if long:
        opt_args.append(long)
    else:
        opt_args.append('--' + name)
    if type == 'bool':
        opt_kwargs['action'] = 'store_true'
    elif type != 'str':
        opt_kwargs['type'] = type
    if default is not None:
        opt_kwargs['default'] = default
    opt_kwargs['help'] = help
    opt_item = optparse.Option(*opt_args, **opt_kwargs)

    def f(g):
        if not hasattr(g, '__optparse_options__'):
            setattr(g, '__optparse_options__', [])
        getattr(g, '__optparse_options__').append(opt_item)
        return g
    return f


class Application:
    def __init__(self, doc=''):
        self.doc = doc
        self.mapping = []

    # 获取最长匹配到path的dealer函数
    # arg_list是不含减号的argv前缀部分
    # 返回path, dealer, level
    def _match_dealer(self, arg_list):
        cur_app = self
        cur_level = 0
        cur_path = ()
        if not arg_list:
            return cur_path, cur_app, cur_level
        while True:
            quit = True
            for path, dealer in cur_app.mapping:
                if arg_list[cur_level] == path:
                    cur_level += 1
                    cur_path += (path,)
                    cur_app = dealer
                    if isinstance(dealer, Application):
                        quit = cur_level == len(arg_list)
                    break
            if quit:
                return cur_path, cur_app, cur_level

    # 获取path的下一级列表即帮助文本
    def _sub_help_doc(self, path, app):  # type: (...) -> str
        cmd = sys.argv[0]
        if '/' in cmd:
            cmd = cmd.rsplit('/', 1)[-1]
        ret = ''
        if app is None:
            app = self
        if not isinstance(app, Application):
            raise ValueError('app must be Application')
        ret += app.doc + '\n'
        for sub_path, dealer in app.mapping:
            ret += '  ' + cmd + ' ' + ' '.join(list(path)) + ' ' + sub_path + '\t\t'
            if isinstance(dealer, Application):
                ret += dealer.doc.strip().splitlines()[0].strip() + '\n'
            else:
                ret += doc_text(dealer).strip().splitlines()[0].strip() + '\n'
        return ret

    def add(self,
            path,  # type: str
            dealer_or_app):
        # type: (...) -> 'Application'
        self.mapping.append((path.strip('/'), dealer_or_app))
        return self

    def run_dealer(self, dealer):
        usage = eafp(lambda: '\n'.join(doc_text(dealer).strip().splitlines()[1:]), '')
        parser = optparse.OptionParser(usage=usage)
        try:
            parser.add_options(getattr(dealer, '__optparse_options__', []))
            options, args = parser.parse_args()
            dealer(*args, **options.__dict__)
        except AssertionError as e:
            if str(e):
                parser.error(str(e) + '!\n')
            else:
                parser.error('-h or --help for help!')

    def run(self):  # type: ('Application') -> None
        list_params = []
        dict_params = {}
        arg_list = sys.argv[1:]
        L = len(arg_list)
        i = 0
        while i < L:
            arg = arg_list[i]
            if arg.startswith('--'):
                assert len(arg) >= 3 and arg[:3] != '---', arg
                arg = arg[2:]
                if '=' in arg:
                    key, value = arg.split('=', 1)
                    dict_params[key] = value
                else:
                    dict_params[arg] = ''
            elif arg.startswith('-'):
                assert len(arg) == 2, arg
                arg = arg[1:]
                if i + 1 >= L or arg_list[i + 1].startswith('-'):
                    dict_params[arg] = ''
                else:
                    dict_params[arg] = arg_list[i + 1]
                    i += 1
            else:
                list_params.append(arg)
            i += 1
        path, dealer, level = self._match_dealer(arg_list)   # 最长匹配
        if dealer is None or isinstance(dealer, Application):
            print(self._sub_help_doc(path, dealer))
            print()
            return
        else:
            usage = eafp(lambda: '\n'.join(doc_text(dealer).strip().splitlines()[1:]), '')
            parser = optparse.OptionParser(usage=usage)
            try:
                parser.add_options(getattr(dealer, '__optparse_options__', []))
                options, args = parser.parse_args(args=arg_list[level:])
                if args:
                    dealer(args=args, **options.__dict__)
                else:
                    dealer(**options.__dict__)
            except AssertionError as e:
                if str(e):
                    parser.error(str(e) + '!\n')
                else:
                    parser.error('-h or --help for help!')


def main():
    text = """
    
    Boilerplate of Installable Project:
        git clone https://github.com/qorzj/lesscli.git

    Documentation of "Writing the Setup Script":
        https://docs.python.org/2/distutils/setupscript.html
        https://docs.python.org/3/distutils/setupscript.html

    Documentation of lesscli.run:
        >>> import lesscli
        >>> help(lesscli.run)

    """
    print(text)
