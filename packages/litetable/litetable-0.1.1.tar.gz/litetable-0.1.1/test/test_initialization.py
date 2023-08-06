from litetable import LiteTable


def test_init_from_list_of_dicts(list_of_dicts):
    dt = LiteTable(list_of_dicts)
    assert len(dt) == len(list_of_dicts)
