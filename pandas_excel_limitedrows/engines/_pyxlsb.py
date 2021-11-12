from pandas.io.excel._pyxlsb import PyxlsbReader
from pandas._typing import (
    FilePathOrBuffer,
    StorageOptions,
    Scalar
)


class PyxlsbLimitedReader(PyxlsbReader):

    def __init__(self, filepath_or_buffer: FilePathOrBuffer, storage_options: StorageOptions = None, max_rows=None):
        self.max_rows = max_rows
        super().__init__(filepath_or_buffer, storage_options=storage_options)

    def get_sheet_data(self, sheet, convert_float: bool):
        data: list[list[Scalar]] = []
        prevous_row_number = -1
        # When sparse=True the rows can have different lengths and empty rows are
        # not returned. The cells are namedtuples of row, col, value (r, c, v).

        rows_enumerate = enumerate(sheet.rows(sparse=True))
        rows_list = []
        if self.max_rows is None:
            rows_list = list(enumerate(sheet.rows(sparse=True)))
        else:
            for i in range(self.max_rows + 1):
                try:
                    rows_list.append(next(rows_enumerate))
                except:
                    break

        for row_number, row in rows_list:
            converted_row = [self._convert_cell(cell, convert_float) for cell in row]
            while converted_row and converted_row[-1] == "":
                # trim trailing empty elements
                converted_row.pop()
            if converted_row:
                data.extend([[]] * (row_number - prevous_row_number - 1))
                data.append(converted_row)
                prevous_row_number = row_number
        if data:
            # extend rows to max_width
            max_width = max(len(data_row) for data_row in data)
            if min(len(data_row) for data_row in data) < max_width:
                empty_cell: list[Scalar] = [""]
                data = [
                    data_row + (max_width - len(data_row)) * empty_cell
                    for data_row in data
                ]
        return data