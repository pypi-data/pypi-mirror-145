# alphav

alpha vantage api wrapper 

# Description
using a symbol object that pulls the data once the property is accessed.   

The data is then saved for the next property calls.     

# Example
```python
from alphav import Symbol

# generate symbple
s = Symbol('IBM', apikey)
# print the data it provides
print(s.balance_sheet)
print(s.earnings)
print(s.income_statement)
print(s.cash_flow)
print(s.overview)
print(s.global_quote)
print(s.time_series_daily)
print(s.time_series_monthly)
print(s.time_series_monthly_adjusted)
print(s.time_series_weekly)
print(s.time_series_weekly_adjusted)
```


The properties are of data object, supporting
```python
# for balance sheet data
prop.main # the main data slice, annual by default
prop.annual # annual data when provieded
prop.quarterly # quarterly data when provided
prop.set_main('quarterly')
prop.main # will be prop.annual

# for the rest of the data
prop.main # only
```

