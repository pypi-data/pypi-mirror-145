import pandas as pd
import pytest

from colassigner import Col, ColAccessor, ColAssigner, get_all_cols


class Multi(ColAccessor):

    a = int
    b = float


def test_simple_annotation_assigner():
    class Simple(ColAccessor):

        ixx = str

    class Cas(ColAssigner):
        def works(self, df) -> Col[Simple]:
            return df.mean(axis=1)

        def with_str(self, df) -> Col[Multi.a]:
            return df.sum(axis=1)

        def no_effect(self, df) -> Col[int]:
            return df.sum(axis=1)

    assert Cas.works == "works__ixx"
    assert Cas.with_str == "with_str__a"
    assert get_all_cols(Cas) == ["no_effect", "with_str__a", "works__ixx"]

    df = pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}).pipe(Cas())
    assert df.loc[:, Cas.works].tolist() == [2, 2, 2]
    assert df.loc[:, Cas.with_str].tolist() == [6, 6, 6]


def test_wrong_annotations():
    with pytest.raises(AssertionError):

        class Wrong(ColAssigner):
            def c1(self, _) -> int:
                pass  # pragma: no cover

        Wrong.c1

    with pytest.raises(ValueError):

        class Wrong2(ColAssigner):
            def thing(self, _) -> Col[Multi]:
                pass  # pragma: no cover

        Wrong2.thing
