import os
import random
from openpyxl import Workbook

from data.config import BASE_DIR


async def purchase_history_excel(data: list[dict]):
    wb = Workbook()
    ws = wb.active
    ws.title = "Purchase History"

    header = data[0].keys()
    ws.append(list(header))

    for row in data:
        ws.append(list(row.values()))

    filename = f"purchase_history_{random.randint(1, 10000)}.xlsx"
    filepath = os.path.join(BASE_DIR, "bot", "documents", filename)

    wb.save(filepath)

    return filepath
