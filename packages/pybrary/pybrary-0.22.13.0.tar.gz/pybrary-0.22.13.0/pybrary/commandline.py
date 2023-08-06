from os import environ
from sys import argv

from pybrary.commandparams import ValidationError


def parse_args(args=None):
    if args:
        opt = args.split()
    else:
        _cmd, *opt = argv

    args, kwds = [], {}
    for o in opt:
        if '=' in o:
            k, v = o.split('=')
            kwds[k] = v
        else:
            args.append(o)
    return args, kwds


class CommandLine:
    config = None
    env_pfx = None

    def __init__(self, *Params):
        params = [P() for P in Params]
        self.specs = {
            p.name: p
            for p in params
        }
        self.positionals = [
            p
            for p in params
            if p.positional
        ]

    @property
    def env_prefix(self):
        def mk(pref):
            if isinstance(pref, str) and pref.strip():
                return f'{pref.strip()}_'
        pref = (
            mk(self.env_pfx)
            or mk(self.config and self.config.get('env_prefix'))
            or ''
        )
        return pref

    def validate(self, *a, **k):
        check = k.pop('_check', False)
        params = dict()
        if len(a) >  len(self.positionals):
            raise ValidationError(f'Too many args : {len(a)}. Expected at most {len(self.positionals)}')
        for v, p in zip(a, self.positionals):
            val = p.check(v) if check else p.validate(v)
            params[p.name] = val
        for name, val in k.items():
            if name in params:
                raise ValidationError(f'{name} is overridding positional arg')
            p = self.specs.get(name)
            if p:
                val = p.check(val) if check else p.validate(val)
                params[name] = val
            else:
                params[name] = '?'
                if not check:
                    raise ValidationError(f'Unsupported arg : {name}')
        for name, p in self.specs.items():
            if name not in params and self.config:
                if name in self.config:
                    v  = self.config[name]
                    val = p.check(v) if check else p.validate(v)
                    params[name] = val
            if name not in params:
                var = f'{self.env_prefix}{name}'
                if var in environ:
                    v = environ[var]
                    val = p.check(v) if check else p.validate(v)
                    params[name] = val
            if name not in params and p.default:
                params[p.name] = p.default
            if name not in params:
                if p.mandatory:
                    params[name] = '!'
                    if not check:
                        raise ValidationError(f'Missing mandatory arg : {p.name}')
                else:
                    params[name] = 'X'
        return params

    def get_params(self, args=None, _check=False):
        a, k = parse_args(args)
        k['_check'] = _check
        params = self.validate(*a, **k)
        return params

    def __call__(self, args=None):
        try:
            params = self.get_params(args)
        except ValidationError as x:
            self.help()
            print(f'\n ! {x}')
            return
        return self.run(params)

    def help(self):
        print(self.__doc__)
        params = self.get_params(_check=True)
        for p in self.specs.values():
            print(f'\n{p.name} = {params[p.name]}')
            p.positional and print(' - Positional')
            p.mandatory and print(' - Mandatory')
            p.default and print(f' - Default : {p.default}')
            lines = [f'    {i}' for i in p.__doc__.strip().split('\n')]
            lines[0] = f'    * {lines[0].strip()} *'
            print('\n'.join(lines))
        print()


class SubCmd:
    config = None
    env_pfx = None

    def __call__(self, args=None):
        if args:
            args = args.split()
        else:
            _cmd, *args = argv

        if args:
            arg = args[0]
            cmd = self.cmds.get(arg)
            if cmd:
                if len(args)>1:
                    return cmd(' '.join(args[1:]))
                else:
                    cmd.help()
                    raise ValidationError(f'\n\n ! Invalid "{arg}" command')

        self.help()
        raise ValidationError(f'\n\n ! Invalid sub command : {args and args[0]}')

    def help(self):
        print(self.__doc__)
        for name, cmd in self.cmds.items():
            print(cmd.__doc__)
