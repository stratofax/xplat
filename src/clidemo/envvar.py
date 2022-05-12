# https://typer.tiangolo.com/tutorial/arguments/envvar/
# This doesn't work with fish?

import typer


def main(name: str = typer.Argument("World", envvar="AWESOME_NAME")):
    typer.echo(f"Hello Mr. {name}")


if __name__ == "__main__":
    typer.run(main)
