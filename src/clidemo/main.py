import typer

# Next: [Printing and Colors - Typer](https://typer.tiangolo.com/tutorial/printing/)


def main(name: str, lastname: str = "", formal: bool = False):
    """
    Say hi to NAME, optionally with a --lastname.

    If --formal is used, say hi very formally.
    """
    if formal:
        typer.echo(f"Good day, kind {name} {lastname}.")
    else:
        typer.echo(f"Hello {name} {lastname}")


if __name__ == "__main__":
    typer.run(main)
