def test_append(lt):
    l = len(lt)
    assert lt[-1] != (11, 12, 13)

    lt.append({
        'c1': 11,
        'c2': 12,
        'c3': 13,
    })
    assert len(lt) == l + 1
    assert lt[-1] == (11, 12, 13)


def test_tuple(lt):
    l = len(lt)
    assert lt[-1] != (11, 12, 13)

    lt.append((11, 12, 13))
    assert len(lt) == l + 1
    assert lt[-1] == (11, 12, 13)


def test_named_tuple(lt_col_names):
    # lt_col_names contains invalid field names for namedtuple. This checks the
    # conversion works.
    assert lt_col_names[0] != lt_col_names[-1]
    row = lt_col_names[0]
    lt_col_names.append(row)
    assert lt_col_names[-1] == lt_col_names[0]
