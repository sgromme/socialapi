def test_addition():
    assert 1 + 1 == 2


def test_dictionary():
    d = {"a": 1, "b": 2}
    expected = {"a": 1}
    assert expected.items() <= d.items()
