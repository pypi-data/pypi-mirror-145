import pytest

from litetable import LiteTable


def test_index(lt):
    # Extracting a single row
    assert isinstance(lt[0], tuple)
    assert lt[0] == lt[0, :]
    assert lt[0] == (1, 2, 3)


def test_negative_index(lt):
    assert lt[-1] == lt[len(lt) - 1]


def test_iteration(lt):
    # Iterating rows
    for row in lt:
        assert sum(row) == 6


def test_sql_where(lt):
    assert list(lt['c1 = 1']) == list(lt[0:2])
    assert list(lt['c1 = 1 OR c1 = 2']) == list(lt[0:4])


def test_slice(lt):
    assert isinstance(lt[0:1], LiteTable)
    assert list(lt[0:1]) == list(lt[0:1, :])
    assert list(lt[:1]) == list(lt[0:1])
    assert list(lt[:-1]) == list(lt[0:len(lt) - 1])
    assert list(lt[-2:-1]) == list(lt[len(lt) - 2:len(lt) - 1])
    assert len(lt[0:2]) == 2
