from colassigner import ColAccessor, get_att_value


def test_type_retention():
    class TestCols(ColAccessor):

        fing = int

        class SubCol(ColAccessor):
            a = int
            b = float

            class SubSubCol(ColAccessor):
                x = str
                y = str

            class SubSubCol2(SubSubCol):
                pass

    assert get_att_value(TestCols, TestCols.fing) == int
    assert get_att_value(TestCols.SubCol, TestCols.SubCol.b) == float
    assert (
        get_att_value(TestCols.SubCol.SubSubCol2, TestCols.SubCol.SubSubCol2.x) == str
    )
