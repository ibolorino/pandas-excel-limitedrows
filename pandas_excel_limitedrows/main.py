
from pandas import ExcelFile
from pandas._typing import StorageOptions
from pandas_excel_limitedrows.engines._openpyxl import OpenpyxlLimitedReader
from pandas_excel_limitedrows.engines._pyxlsb import PyxlsbLimitedReader
from pandas_excel_limitedrows.engines._xlrd import XlrdLimitedReader

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
        io = RowLimitedExcelFile(io, storage_options=storage_options, engine=engine, max_rows=max_rows)
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
    def __init__(self, path_or_buffer, engine=None, storage_options: StorageOptions = None, max_rows=None):
        self.max_rows = max_rows
        self._engines.update(
            {
                "openpyxl": OpenpyxlLimitedReader,
                "pyxlsb": PyxlsbLimitedReader,
                "xlrd": XlrdLimitedReader,
            }
        )

        super().__init__(path_or_buffer, engine, storage_options)
        self._reader = self._engines[self.engine](self._io, storage_options=storage_options, max_rows=self.max_rows)
        return