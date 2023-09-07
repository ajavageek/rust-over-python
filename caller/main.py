import click
from ctypes import c_double, CDLL, Structure
from typing import Optional

rust = CDLL('../callee/target/debug/libcomplex.dylib')


class RustComplex(Structure):
    _fields_ = [("re", c_double),
                ("im", c_double)]


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
    print(complex(result.re, result.im))


def call_service(n1: complex, n2: complex, command: str) -> RustComplex:
    rust.compute.restype = RustComplex
    return rust.compute(command.encode("UTF-8"), c_double(n1.real), c_double(n1.imag), c_double(n2.real),
                        c_double(n2.imag))


if __name__ == '__main__':
    cli()
