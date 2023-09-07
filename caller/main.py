import json
import socket
from typing import Optional
import click


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
    with socket.socket(socket.AF_UNIX) as client:
        data: dict[str, list[float]] = dict(command=command,a=[n1.real, n1.imag], b=[n2.real, n2.imag])
        encoded: bytes = json.dumps(data).encode('UTF-8')
        print(f'Sent: {encoded}')
        client.connect("/tmp/socket")
        client.send(encoded)
        result: bytes = client.recv(0)
        print(f'Received: {result}')
        client.close()
        match command:
            case 'add': return n1 + n2
            case 'sub': return n1 - n2
            case 'mul': return n1 * n2


if __name__ == '__main__':
    cli()
