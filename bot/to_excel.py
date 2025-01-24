import os
import random
from datetime import datetime, timedelta
from openpyxl import Workbook
from data.config import BASE_DIR

async def purchase_history_excel(data: list[dict]):
    """
    Creates an Excel file containing purchase history from the provided data.

    :param data: A list of dictionaries representing purchase history.
    :return: The file path of the generated Excel file or None if no data is provided.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Purchase History"

    if len(data) > 0:
        # Add headers to the Excel sheet
        ws.append(["Redeem-kod", "UC Paket", "Balans turi", "Harid vaqti"])

        for row in data:
            values = list(row.values())

            # Convert balance type to uppercase
            values[2] = values[2].upper()

            # Adjust and format the datetime (adding 5 hours)
            adjusted_dt = datetime.fromisoformat(str(values[3])) + timedelta(hours=5)
            values[3] = adjusted_dt.strftime('%H:%M:%S %d-%m-%Y')

            # Append formatted row to the Excel sheet
            ws.append([str(value) for value in values])

        # Generate a random filename
        filename = f"purchase_history_{random.randint(1, 10000)}.xlsx"
        filepath = os.path.join(BASE_DIR, "bot", "documents", filename)

        # Save the Excel file
        wb.save(filepath)

        return filepath
    else:
        return None
