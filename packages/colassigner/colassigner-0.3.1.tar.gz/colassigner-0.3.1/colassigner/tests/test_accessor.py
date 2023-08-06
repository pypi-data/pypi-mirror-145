from colassigner import ColAccessor, get_all_cols


def test_flat_accessor():
    class Cols(ColAccessor):
        x = int
        a = float

    assert Cols.x == "x"
    assert Cols.a == "a"


def test_nested_accessor():
    class GrandChildCols(ColAccessor):
        x = str
        y = str

    class ChildCols(ColAccessor):
        a = int
        b = float
        grandchild_a = GrandChildCols
        grandchild_b = GrandChildCols

    class Cols(ColAccessor):

        fing = int
        assigned_child = ChildCols

        class InheritedChild(ChildCols):
            pass

    assert Cols.fing == "fing"
    assert Cols.assigned_child.a == "assigned_child__a"
    assert Cols.assigned_child.grandchild_a.x == "assigned_child__grandchild_a__x"
    assert Cols.assigned_child.grandchild_b.y == "assigned_child__grandchild_b__y"
    assert Cols.InheritedChild.b == "inherited_child__b"

    assert get_all_cols(Cols) == [
        "inherited_child__a",
        "inherited_child__b",
        "inherited_child__grandchild_a__x",
        "inherited_child__grandchild_a__y",
        "inherited_child__grandchild_b__x",
        "inherited_child__grandchild_b__y",
        "assigned_child__a",
        "assigned_child__b",
        "assigned_child__grandchild_a__x",
        "assigned_child__grandchild_a__y",
        "assigned_child__grandchild_b__x",
        "assigned_child__grandchild_b__y",
        "fing",
    ]

    assert get_all_cols(Cols.assigned_child) == [
        "assigned_child__a",
        "assigned_child__b",
        "assigned_child__grandchild_a__x",
        "assigned_child__grandchild_a__y",
        "assigned_child__grandchild_b__x",
        "assigned_child__grandchild_b__y",
    ]


def test_accessor_id_cols():
    class IdCols(ColAccessor):

        fing_id = int
        other_id = str

    class TableCols(ColAccessor):

        foreign_key = IdCols.fing_id

    assert TableCols.foreign_key == "foreign_key"
