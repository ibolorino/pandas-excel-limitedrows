from pandas.io.excel._openpyxl import OpenpyxlReader
from pandas import ExcelFile
from pandas._typing import (
    FilePathOrBuffer,
    StorageOptions,
    DtypeArg
)

# TODO: Implementar parâmetros first_rows e last_rows - 1.2.0

def read_excel(
    io,
    sheet_name=0,
    header=0,
    names=None,
    index_col=None,
    usecols=None,
    squeeze=False,
    dtype=None,
    engine=None,
    converters=None,
    true_values=None,
    false_values=None,
    skiprows=None,
    nrows=None,
    na_values=None,
    keep_default_na=True,
    na_filter=True,
    verbose=False,
    parse_dates=False,
    date_parser=None,
    thousands=None,
    comment=None,
    skipfooter=0,
    convert_float=None,
    mangle_dupe_cols=True,
    storage_options: StorageOptions = None,
    max_rows=None
):

    should_close = False
    if not isinstance(io, RowLimitedExcelFile):
        should_close = True
        io = RowLimitedExcelFile(io, storage_options=storage_options, engine="row_limited", max_rows=max_rows)
    elif engine and engine != io.engine:
        raise ValueError(
            "Engine should not be specified when passing "
            "an ExcelFile - ExcelFile already has the engine set"
        )
    
    if max_rows and max_rows < 0:
        raise ValueError(
            "max_rows parameter must be greater or equal to 0"
        )

    try:
        data = io.parse(
            sheet_name=sheet_name,
            header=header,
            names=names,
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype=dtype,
            converters=converters,
            true_values=true_values,
            false_values=false_values,
            skiprows=skiprows,
            nrows=nrows,
            na_values=na_values,
            keep_default_na=keep_default_na,
            na_filter=na_filter,
            verbose=verbose,
            parse_dates=parse_dates,
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    finally:
        # make sure to close opened file handles
        if should_close:
            io.close()
    return data




class RowLimitedExcelFile(ExcelFile):
    def __init__(self, path_or_buffer, engine="row_limited", storage_options: StorageOptions = None, max_rows=None):
        self.max_rows = max_rows
        self._engines.update({"row_limited": RowLimitedReader})
        super().__init__(path_or_buffer, engine, storage_options)
        self._reader = self._engines[engine](self._io, storage_options=storage_options, max_rows=self.max_rows)
        return


class RowLimitedReader(OpenpyxlReader):

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