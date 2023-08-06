# LiteTable 

`LiteTable` makes working with data tables convenient in Python.  Avoid having 
to (re)learn yet another syntax for structured data queries if 
you already know SQL and like the way `numpy` and/or the `data.table` in R 
work. `LiteTable` aims to behave as you would intuitively expect. 

Under the hood, the SQL is powered by SQLite via a thin layer over the 
`sqlite3` package.


## Usage

The following examples show how to use LiteTable data tables.

### Create LiteTable object

```python
from litetable import LiteTable

data = [
    {
        'a': 1,
        'b': 2,
        'c': 3
    },
    {
        'a': 4,
        'b': 5,
        'c': 6
    }
]

lt = LiteTable(data)
```

### Append

```python
# The row object can be dict or tuple
lt.append(row)
```

### Access rows

In `LiteTable` the first dimension pinpoints the row as in `numpy`. Bare 
indices return rows and slices return new `LiteTable` objects.

```python
# Using index returns the row data in a (named) tuple
lt[0]  # -> tuple

# Using a slice returns the rows in a new LiteTable object
lt[0:2]  #-> LiteTable

# Using SQL. Write the WHERE clause in the brackets a bit like in `data.table`.
lt['b = 2']  # -> LiteTable

# Iterating LiteTable object iterates the rows
for row in lt:
    # row is a (named) tuple
    pass
```

### Access columns

Think `LiteTable` as a two dimensional numpy array, where the second dimension
is the column. Access just like in `numpy`, or with SQL in a similar way as in
`data.table`.

```python
# Get column data with the column index with numpy style 2d array access
lt[:, 1]  # -> list

# Get the index by the column name
lt[:, lt.index('b')]  # -> list

# Getting columns as a slice returns a new LiteTable
lt[:, 0:2]  # -> LiteTable

# Getting columns with column name slice. Note that this returns also column c.
lt[:, 'a':'c']  # -> LiteTable

# Using SQL to get and transform column(s) with the SELECT clause.
lt[:, 'a + b as sum']  # -> LiteTable

# Get column b directly by the name
lt.b  # -> list

# Get column '% of uses' without having to quote it
lt.col('% of users')
```

### Access rows and columns simultaneusly

```python
# Numpy style
lt[0:2, 1:3]  # -> LiteTable

# SQL style
lt['c = 2', 'c, a + b as sum']  # -> LiteTable

# Mix and match. Get c and a + b for row 1.
lt[1, 'c, a + b as sum']  # -> tuple

# Want access to the data directly instead? Request an iterator
# TO BE IMPLEMENTED
lt['c = 2', iter]  # -> Iterable

# Iterate dicts
# TO BE IMPLEMENTED
lt['c = 2', dict]

# Iterate bare tuples (unnamed)
# TO BE IMPLEMENTED
lt['c = 2', tuple]
```

### Group by

```python 
# The third argument is the GROUP BY clause.
lt[:, 'c, sum(a + b) as total', 'c']  # -> tuple
```

### Transform the LiteTable with SQL SELECT statements

```python
# Note that :this is a placeholder for the SQLite table name holding the data
lt('SELECT * FROM :this')  # -> LiteTable
```

### Execute arbitrary SQL

```python
lt.execute('UPDATE :this SET a=1 WHERE c=3')  # -> Cursor object
```

### Access directly the SQLite connection object

```python
lt.conn
```

### Pandas conversion
If you need a Pandas dataframe just convert either way. Note that e.g. the 
date objects from Pandas won't survive the conversion to `LiteTable` and back.

```python
import pandas as pd

df = pd.DataFrame(lt)
lt = LiteTable(df)

```

## TODO

`LiteTable` is still in early development, so there are lots of things still to 
do, and glitches/bugs to be found.

- Improve (i.e. prettify) `__repr__`
- Proper tests for arguments on LiteTable creation
- Joins
- Optimizations with SQL transactions
- Conversion into (`numpy`) array
- Think the casting of different types
- Iterate dicts, bare tuples, etc.
- Comparisons `lt1 == lt2`
- Static analysis
