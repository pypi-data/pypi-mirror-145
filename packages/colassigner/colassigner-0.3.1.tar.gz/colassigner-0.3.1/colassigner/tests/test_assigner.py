import numpy as np
import pandas as pd
from pytest import raises

from colassigner import ChildColAssigner, ColAssigner, get_all_cols


def test_flat_assigner():
    class Cols(ColAssigner):
        def col_a(self, df):
            return df.iloc[:, -1] * 2

        def acol(self, df):
            return df.loc[:, Cols.col_a] - 1

    assert Cols.col_a == "col_a"
    assert Cols.acol == "acol"
    assert get_all_cols(Cols) == ["acol", "col_a"]  # alphabetical

    df = pd.DataFrame({"a": [1, 2, 3]}).pipe(Cols())
    assert df.loc[:, Cols.col_a].tolist() == [2, 4, 6]
    assert df.loc[:, Cols.acol].tolist() == [1, 3, 5]


def test_inited_assigner():
    class Cols(ColAssigner):
        def __init__(self, n) -> None:
            self.n = n

        def col(self, df):
            return (df < self.n).all(axis=1)

    df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 0, 1]}).pipe(Cols(3))
    assert df.loc[:, Cols.col].tolist() == [False, True, False]
    assert get_all_cols(Cols) == ["col"]


def test_wrong_colname():
    with raises(ValueError):

        class ColW(ColAssigner):
            def mro(self, df):
                return 4  # pragma: nocover


def test_child_assigner():
    class AssChild(ChildColAssigner):
        def nothing(self):
            return False

    class Cols(ColAssigner):
        def col_one(self, df):
            return 1

        class SubCol(ColAssigner):
            def fing(self, df):
                return df.sum(axis=1)

            class SubSubCol(ColAssigner):
                _prefix = "pref_"

                def sub_x(self, df):
                    return 0

                def sub_y(self, df):
                    return self._prefix + df[Cols.col_one].astype(str)

            class SubSubCol2(SubSubCol):
                _prefix = "pref2_"

        sep_child = AssChild

    assert Cols.SubCol.fing == "sub_col__fing"
    assert Cols.SubCol.SubSubCol.sub_x == "sub_col__sub_sub_col__sub_x"
    assert Cols.SubCol.SubSubCol2.sub_y == "sub_col__sub_sub_col_2__sub_y"
    assert get_all_cols(Cols) == [
        "sub_col__sub_sub_col__sub_x",
        "sub_col__sub_sub_col__sub_y",
        "sub_col__sub_sub_col_2__sub_x",
        "sub_col__sub_sub_col_2__sub_y",
        "sub_col__fing",
        "col_one",
        "sep_child__nothing",
    ]

    df = pd.DataFrame({"a": [1, 2, 3]}).pipe(Cols())
    assert (df.loc[:, Cols.SubCol.fing] == (df["a"] + df[Cols.col_one])).all()
    assert (df[Cols.SubCol.SubSubCol2.sub_y] == "pref2_1").all()


def test_subassigner_data_reuse():
    class IntSides(ChildColAssigner):
        def __init__(self, df, parent_assigner: "GbReindex") -> None:
            self.arr = parent_assigner.arr

        def lower(self):
            return np.floor(self.arr).astype(int)

        def upper(self):
            return np.ceil(self.arr).astype(int)

    class GbReindex(ChildColAssigner):
        main_col = ...

        def __init__(self, df, bc: "BaseCols"):
            self.arr = bc.base_gb.reindex(df[self.main_col]).values

        def values(self):
            return self.arr

        sides = IntSides

    class BaseCols(ColAssigner):
        def __init__(self, base_df):
            self.base_gb = base_df.groupby("cat")["num"].mean()

        class GbB(GbReindex):
            main_col = "b"

        class GbC(GbReindex):
            main_col = "c"

        def prod(self, df):
            return df.loc[:, [BaseCols.GbB.sides.lower, BaseCols.GbC.values]].prod(
                axis=1
            )

    df1 = pd.DataFrame({"cat": ["x", "y", "y"], "num": [2, 3, 4]})
    # add mean of category, with lower and upper bounds
    # for 2 different columns, add product of two of these
    df2 = pd.DataFrame({"b": ["x", "y", "x"], "c": ["y", "y", "x"]}).pipe(BaseCols(df1))

    assert df2.loc[:, BaseCols.GbB.values].tolist() == [2, 3.5, 2]
    assert df2.loc[:, BaseCols.GbC.sides.lower].tolist() == [3, 3, 2]
    assert df2.loc[:, BaseCols.GbC.sides.upper].tolist() == [4, 4, 2]
    assert df2.loc[:, BaseCols.prod].tolist() == [7, 10.5, 4]
