import click
from ctypes import c_double, CDLL, Structure
from typing import Optional, Any

rust = CDLL('../callee/target/debug/libcomplex.dylib')


class RustComplex(Structure):
    _fields_ = [("re", c_double),
                ("im", c_double)]

    def __init__(self, c: complex, *args: Any, **kw: Any) -> None:
        super().__init__(*args, **kw)
        self.re = c.real
        self.im = c.imag

    def to_complex(self) -> complex:
        return complex(self.re, self.im)


@click.command()
@click.option('--add', 'command', flag_value='add')
@click.option('--sub', 'command', flag_value='sub')
@click.option('--mul', 'command', flag_value='mul')
@click.option('--arg1', help='First complex number in the form x+yj')
@click.option('--arg2', help='Second complex number in the form x\'+y\'j')
def cli(command: Optional[str], arg1: Optional[str], arg2: Optional[str]) -> None:
    n1: complex = complex(arg1)
    n2: complex = complex(arg2)
    result: RustComplex = call_service(n1, n2, command)
    print(result.to_complex())


def call_service(n1: complex, n2: complex, command: str) -> RustComplex:
    rust.compute.restype = RustComplex
    return rust.compute(command.encode("UTF-8"), RustComplex(n1), RustComplex(n2))


if __name__ == '__main__':
    cli()
