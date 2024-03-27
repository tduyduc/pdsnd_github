# US Bike Share Data Exploration

### Date created

2024/03/28

### Description

An interactive environment where you can view bike share data insights for a few US cities. Data can also be refined by time range.

### Environment

This project requires Python 3.10 or later. Pandas is also required, and can be installed via:

```shell
pip install pandas
```

Data files are also necessary (see _Files used_ section below).

### Files used

- `bikeshare.py`
- `chicago.csv`
- `new_york_city.csv`
- `washington.csv`

### References

- General Python coding
  - [Prevent pycodestyle linter from complaining long docstrings](https://github.com/PyCQA/pycodestyle/issues/224)
  - [Type annotation (this was intentional, given my Java and TypeScript programming background which prefers explicit, static typing)](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- Pandas
  - [Indexing with a lambda expression](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#selection-by-callable)
  - [What if I forget to convert data to Timestamp](https://stackoverflow.com/questions/33365055/attributeerror-can-only-use-dt-accessor-with-datetimelike-values)
  - [Get month from series data's timestamp](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.month.html)
  - [Map a column](https://stackoverflow.com/questions/43356704/map-dataframe-index-using-dictionary)
  - [Group by for counting](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.groupby.html)
  - [Convert time difference to seconds](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.total_seconds.html)
  - [Find the most frequent combination in a DataFrame](https://stackoverflow.com/questions/63229237/finding-the-most-frequent-combination-in-dataframe)

### Known bugs

None yet. If you find any, please file an issue.
