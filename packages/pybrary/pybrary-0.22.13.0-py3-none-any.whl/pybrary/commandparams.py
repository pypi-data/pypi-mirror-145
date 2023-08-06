from pathlib import Path


class ValidationError(Exception):
    '''Validation Error'''


class Param:
    name = None
    positional = False
    mandatory = False
    default = None

    def __init__(self):
        if not self.name:
            raise ValueError(
                f'"{self.__class__.__name__}" Param sould have a "name" attribute'
            )
        self.value = None
        self.validated = None

    def verify(self):
        return self.value

    def validate(self, value):
        self.value = value
        self.validated = self.verify()
        return self.validated

    def check(self, val):
        try:
            v = self.validate(val)
        except ValidationError as x:
            v = f' ! {val} !'
        return v


class ParamInt(Param):
    def verify(self):
        try:
            return int(self.value)
        except Exception as x:
            raise ValidationError(f'{self.value}') from x


class ParamPath(Param):
    def __init__(self, *a, **k):
        self.create = k.pop('create', False)
        super().__init__(*a, **k)


class ParamFile(ParamPath):
    def verify(self):
        try:
            path = Path(self.value)
        except Exception as x:
            raise ValidationError(f'{self.value}') from x
        if path.is_file():
            return path
        elif self.create:
            try:
                path.open('x')
            except Exception as x:
                raise ValidationError(f'{self.value}') from x
        else:
            raise ValidationError(f'"{self.name}" File not found : {self.value}')


class ParamDir(ParamPath):
    def verify(self):
        try:
            path = Path(self.value)
        except Exception as x:
            raise ValidationError(f'\n{self.value}') from x
        if path.is_dir():
            return path
        elif self.create:
            try:
                path.mkdir(parents=True)
            except Exception as x:
                raise ValidationError(f'{self.value}') from x
        elif path.exists():
            raise ValidationError(f'"{self.name}" : {self.value} is not a dir')
        else:
            raise ValidationError(f'"{self.name}" dir not found : {self.value}')
