import pytest

from litetable import LiteTable


def test_index(lt):
    # Extracting a single column. Note that it's a list extracted from the row
    # tuples
    assert lt[:, 0] == [1, 1, 2, 2, 3, 3]
    assert lt[:, 2] == [3, 2, 3, 1, 2, 1]
    assert list(lt[:, lt.index('c3')]) == list(lt[:, 2])


def test_attribute(lt):
    assert lt.c3 == [3, 2, 3, 1, 2, 1]
    with pytest.raises(AttributeError):
        lt.c4


def test_col_method(lt, lt_col_names):
    assert lt.col('c3') == [3, 2, 3, 1, 2, 1]
    with pytest.raises(ValueError):
        lt.col('c4')

    assert lt_col_names.col('% of total') == [0.1, 0.2, 0.3]


def test_sql_select(lt):
    assert isinstance(lt[:, 'c2'], LiteTable)
    assert list(lt[:, 'c1']) == [(1,), (1,), (2,), (2,), (3,), (3,)]

    lt = lt[:, 'c1, c1 + c2 + c3 as sum']
    assert lt.columns == ['c1', 'sum']
    assert list(lt) == [(1, 6), (1, 6), (2, 6), (2, 6), (3, 6), (3, 6)]


def test_slice(lt):
    assert list(lt[:, 'c2, c3']) == list(lt[:, 1:3])


def test_string_slice(lt):
    assert list(lt[:, 'c1':'c2']) == list(lt[:, :2])
