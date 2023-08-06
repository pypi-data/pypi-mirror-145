from typing import List

from beautifultable import BeautifulTable
from beautifultable.enums import STYLE_BOX_ROUNDED


def make_table(header: List[str], content: List[List[str]]):
    table = BeautifulTable()
    table.columns.header = header
    for row in content:
        table.rows.append(row)
    table.set_style(STYLE_BOX_ROUNDED)
    table.columns.header.separator = '═'
    table.columns.header.junction = '╪'
    table.border.header_left = '╞'
    table.border.header_right = '╡'
    return str(table)
