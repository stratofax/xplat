import typer

# Next: [Printing and Colors - Typer](https://typer.tiangolo.com/tutorial/printing/)


def main(name: str, lastname: str = "", formal: bool = False):
    """
    Say hi to NAME, optionally with a --lastname.

    If --formal is used, say hi very formally.
    """
    if formal:
        typer.secho(f"Good day, kind {name} {lastname}.", fg=typer.colors.BRIGHT_YELLOW)
    else:
        typer.secho(f"Hello {name} {lastname}", fg=typer.colors.BRIGHT_CYAN)


if __name__ == "__main__":
    typer.run(main)
