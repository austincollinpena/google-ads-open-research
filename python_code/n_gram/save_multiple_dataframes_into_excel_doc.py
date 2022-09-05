import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from typing import TypedDict
from tempfile import NamedTemporaryFile
import uuid


class DFAndName(TypedDict):
    df: pd.DataFrame
    campaign: str
    gram_count: int


def save_multiple_dataframes_into_excel_doc(dfs: list[pd.DataFrame], save_locally: bool, account_name: str) -> NamedTemporaryFile:
    """
    :param dfs: list of dataframes to save
    :param save_locally: tells the function either save the workbook locally or not
    :param account_name: helps name the file
    :return:
    """
    wb = Workbook()
    for df in dfs:
        if df.empty:
            continue

        campaign_name = df.iloc[0]['Campaign']
        gram_count = df.iloc[0]['gram_count']
        df = df.sort_values(by=['n_gram_count'], ascending=False)
        name = ""
        if len(campaign_name) > 20:
            name = f'{campaign_name[0:19]}-{gram_count}-gram'
        else:
            name = f'{campaign_name}-{gram_count}-gram'
        name = name.replace("/", "-")
        current_sheet = wb.create_sheet(name)
        rows = dataframe_to_rows(df)
        for r_idx, row in enumerate(rows, 1):
            for c_idx, value in enumerate(row, 1):
                current_sheet.cell(row=r_idx, column=c_idx, value=value)

    if save_locally:
        wb.save(f'./n_gram/git_ignored_data/processed_files/{account_name}.xlsx')
        return

    with NamedTemporaryFile(delete=False) as tmp:
        wb.save(tmp.name)
        tmp.seek(0)
        tmp.name = f'{account_name}-{uuid.uuid4()}.xlsx'
        return tmp
