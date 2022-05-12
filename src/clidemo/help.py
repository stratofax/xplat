# https://typer.tiangolo.com/tutorial/arguments/help/

import typer


def main(
    name: str = typer.Argument(
        "World", help="The name of the user to greet", metavar="✨username✨"
    )
):
    """
    Say hi to NAME very gently
    """
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
