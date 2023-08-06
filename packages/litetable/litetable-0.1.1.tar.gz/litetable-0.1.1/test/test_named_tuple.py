def test_single_row(lt):
    assert lt[3].c1 == 2


def test_iterate_rows(lt):
    for row in lt:
        pass
