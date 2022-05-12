# https://typer.tiangolo.com/tutorial/options/help/

import typer


def main(
    name: str,
    lastname: str = typer.Option("", help="Last name of person to greet."),
    formal: bool = typer.Option(False, help="Say hi fomrally."),
):
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
