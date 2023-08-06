

def test_this(lt):
    lt = lt('select c1 from :this')
    assert len(lt) == 6
    assert lt[:, 0] == [1, 1, 2, 2, 3, 3]


def test_sql(lt, lt_c2_sum_c1):
    lt = lt('select c2, sum(c1) as sum_c1 from :this group by c2 order by c2')
    assert len(lt) == 3
    assert list(lt) == [(1, 5), (2, 4), (3, 3)]
    assert list(lt) == list(lt_c2_sum_c1)


def test_execute(lt):
    assert lt[0, 0] == 1
    lt.execute('UPDATE :this SET c1 = 0 WHERE c2 = 2')
    assert lt[0, 0] == 0
