"post a csv on google 💩"
from pathlib import Path
from sys import stdin

import typer
from gspread import authorize

from .tools import auth, write_in_sheet

app = typer.Typer()


@app.command()
def update(
    url: str = typer.Argument(None, envvar="GSP_URL"),
    token_path: Path = typer.Option(
        Path("~/.local/share/gsp/token.json").expanduser(), envvar="GSP_TOKEN_PATH"
    ),
    creds_path: Path = typer.Option(
        Path("~/.local/share/gsp/credentials.json").expanduser(),
        envvar="GSP_CREDENTIALS_PATH",
    ),
    sheet: int = typer.Option(
        0, envvar="GSP_SHEET", help="Index of the sheet to write"
    ),
    line: int = typer.Option(
        1, envvar="GSP_LINE", help="Number of the line where writing starts"
    ),
    col: int = typer.Option(
        1, envvar="GSP_COL", help="Number of the col where writing starts"
    ),
) -> None:
    """Read a CSV on stdin and post it on an existing google 💩"""
    creds = auth(token_path, creds_path)
    client = authorize(creds)

    doc = client.open_by_url(url)
    write_in_sheet(stdin, doc, sheet, line, col)

    print(doc.url)


@app.command()
def create(
    title: str = typer.Argument("new sheet", envvar="GSP_TITLE"),
    token_path: Path = typer.Option(
        Path("~/.local/share/gsp/token.json").expanduser(), envvar="GSP_TOKEN_PATH"
    ),
    creds_path: Path = typer.Option(
        Path("~/.local/share/gsp/credentials.json").expanduser(),
        envvar="GSP_CREDENTIALS_PATH",
    ),
    sheet: int = typer.Option(
        0, envvar="GSP_SHEET", help="Index of the sheet to write"
    ),
    line: int = typer.Option(
        1, envvar="GSP_LINE", help="Number of the line where writing starts"
    ),
    col: int = typer.Option(
        1, envvar="GSP_COL", help="Number of the col where writing starts"
    ),
) -> None:
    """Read a CSV on stdin and post a CSV on new google 💩"""
    creds = auth(token_path, creds_path)
    client = authorize(creds)

    doc = client.create(title)
    write_in_sheet(doc, sheet, line, col)

    print(doc.url)


if __name__ == "__main__":
    app()
