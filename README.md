# Description

Pandas Excel LimitedRows is a Python library used to optimize the Pandas's read_excel function, adding a max_row parameter if you need to read only the X first lines.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install pandas-excel-limitedrows
```

## Usage

```python
import pandas_excel_limitedrows as pdlr

# Generate DataFrame with first 50 rows
df = pdlr.read_excel(file, max_rows=50)

# Instanciate ExcelFile with first 50 rows
excel_file = pdlr.RowLimitedExcelFile(file, max_rows=50) 
```
Notes: 
- If you use sheet_name as list to read more than one sheet, all dataframes will be generated with max_rows limit;
- All others pandas.read_excel() and pandas.ExcelFile() parameters can be used;
- This package uses Pandas, OpenpyXL, Pyxlsb and Xlrd dependencies and works these three engines.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)