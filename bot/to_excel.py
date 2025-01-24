import os
import random
import datetime

from openpyxl import Workbook
from data.config import BASE_DIR


async def purchase_history_excel(data: list[dict]):
    wb = Workbook()
    ws = wb.active
    ws.title = "Purchase History"

    if not len(data) == 0:
        ws.append(["Redeem-kod", "UC Paket", "Balans turi", "Harid vaqti"])

        for row in data:
            values = list(row.values())
            values[2] = values[2].upper()

            adjusted_dt: datetime.datetime = values[3] + datetime.timedelta(hours=5)            
            values[3] = adjusted_dt.strftime('%S:%M:%H %d-%m-%Y')

            ws.append([str(value) for value in values])

        filename = f"purchase_history_{random.randint(1, 10000)}.xlsx"
        filepath = os.path.join(BASE_DIR, "bot", "documents", filename)

        wb.save(filepath)

        return filepath
    else:
        return None
