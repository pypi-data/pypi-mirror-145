def test_group_by(lt):
    ltg = lt[:, 'c1, sum(c2) as sum_c2', 'c1']
    assert len(ltg) == 3
    assert ltg[:, ltg.index('sum_c2')] == [5, 4, 3]


def test_with_where(lt):
    ltg = lt['c1 = 1 OR c1 = 2', 'c1, sum(c2) as sum_c2', 'c1']
    assert len(ltg) == 2
    assert ltg[:, ltg.index('sum_c2')] == [5, 4]


def test_with_slice(lt):
    ltg = lt[0:3, 'c1, sum(c2) as sum_c2', 'c1']
    assert len(ltg) == 2
    assert ltg[:, ltg.index('sum_c2')] == [5, 1]
