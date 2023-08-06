from csv import reader
from io import TextIOBase
from pathlib import Path
from typing import Iterable, Iterator

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from gspread.cell import Cell
from gspread.spreadsheet import Spreadsheet


def iter_cell(
    value_iterator: Iterable[Iterable[str]], start_row: int, start_col: int
) -> Iterator[Cell]:
    for row, line in enumerate(value_iterator, start=start_row):
        for col, value in enumerate(line, start=start_col):
            yield Cell(row, col, value)


def auth(token_path: Path, creds_path: Path) -> Credentials:
    scopes = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets",
    ]

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(token_path, scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, scopes)
            creds = flow.run_local_server(port=0)

        with token_path.open("w") as token:
            token.write(creds.to_json())

    return creds


def write_in_sheet(
    input_: TextIOBase, doc: Spreadsheet, sheet: int = 0, line: int = 1, col: int = 1
) -> None:
    """Write sheet content"""
    worksheet = doc.get_worksheet(sheet)
    csvreader = reader(iter(input_.readline, ""))

    worksheet.update_cells(tuple(iter_cell(csvreader, line, col)))
