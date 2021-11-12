from pandas.io.excel._openpyxl import OpenpyxlReader
from pandas._typing import (
    FilePathOrBuffer,
    StorageOptions,
    Scalar
)

class OpenpyxlLimitedReader(OpenpyxlReader):

    def __init__(self, filepath_or_buffer: FilePathOrBuffer, storage_options: StorageOptions = None, max_rows=None) -> None:
        self.max_rows = max_rows
        super().__init__(filepath_or_buffer, storage_options=storage_options)

    def get_sheet_data(self, sheet, convert_float: bool):
        if self.book.read_only:
            sheet.reset_dimensions()

        data: list[list[Scalar]] = []
        last_row_with_data = -1

        rows_enumerate = enumerate(sheet.rows)
        rows_list = []
        if self.max_rows is None:
            rows_list = list(enumerate(sheet.rows))
        else:
            for i in range(self.max_rows + 1):
                try:
                    rows_list.append(next(rows_enumerate))
                except:
                    break
        for row in rows_list:
            converted_row = [self._convert_cell(cell, convert_float) for cell in row[1]]
            while converted_row and converted_row[-1] == "":
                # trim trailing empty elements
                converted_row.pop()
            if converted_row:
                last_row_with_data = row[0]
            data.append(converted_row)
        
        # Trim trailing empty rows
        data = data[: last_row_with_data + 1]
        if len(data) > 0:
            # extend rows to max width
            max_width = max(len(data_row) for data_row in data)
            if min(len(data_row) for data_row in data) < max_width:
                empty_cell: list[Scalar] = [""]
                data = [
                    data_row + (max_width - len(data_row)) * empty_cell
                    for data_row in data
                ]
        return data