
def test_element_access(lt):
    assert lt[0, 0] == 1
    assert lt[1, 1] == 3


def test_no_op(lt):
    assert list(lt[:, '*']) == list(lt)
    assert list(lt[:, :]) == list(lt)
