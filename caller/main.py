from typing import Optional
import click
import requests


@click.command()
@click.option('--add', 'command', flag_value='add')
@click.option('--sub', 'command', flag_value='sub')
@click.option('--mul', 'command', flag_value='mul')
@click.option('--arg1', help='First complex number in the form x+yj')
@click.option('--arg2', help='Second complex number in the form x\'+y\'j')
def cli(command: Optional[str], arg1: Optional[str], arg2: Optional[str]) -> None:
    n1: complex = complex(arg1)
    n2: complex = complex(arg2)
    result: complex = call_service(n1, n2, command)
    print(result)


def call_service(n1: complex, n2: complex, command: str) -> complex:
    json: dict[str, list[float]] = dict(a=[n1.real, n1.imag], b=[n2.real, n2.imag])
    req = requests.post(f'http://localhost:3000/{command}', json=json)
    body: dict[str: list[float]] = req.json()
    print(body)
    if body and 'result' in body:
        real: Optional[str] = body['result'][0]
        imaginary: Optional[str] = body['result'][1]
        return complex(float(real), float(imaginary))
    raise Exception()


if __name__ == '__main__':
    cli()
