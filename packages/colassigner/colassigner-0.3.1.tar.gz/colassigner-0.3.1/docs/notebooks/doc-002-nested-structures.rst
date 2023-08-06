Nested Structures
=================

Nested Accessor
---------------

.. code:: ipython3

    import pandas as pd

.. code:: ipython3

    from colassigner import ColAccessor

.. code:: ipython3

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

.. code:: ipython3

    pd.DataFrame(
        {
            Cols.fing: [2, 3, 4],
            Cols.assigned_child.grandchild_a.y: ["a", "b", "c"],
            Cols.InheritedChild.b: [0.1, 0.2, 0.3],
        }
    )




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>fing</th>
          <th>assigned_child__grandchild_a__y</th>
          <th>inherited_child__b</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>2</td>
          <td>a</td>
          <td>0.1</td>
        </tr>
        <tr>
          <th>1</th>
          <td>3</td>
          <td>b</td>
          <td>0.2</td>
        </tr>
        <tr>
          <th>2</th>
          <td>4</td>
          <td>c</td>
          <td>0.3</td>
        </tr>
      </tbody>
    </table>
    </div>



Nested Assigner
---------------

.. code:: ipython3

    from colassigner import ColAssigner

.. code:: ipython3

    class SourceCols(ColAccessor):
        
        x = float
        b = bool
    
    class SepChild(ColAssigner):
        _col = SourceCols.x
        
        def neg(self, df):
            return -df[self._col]
        
        def double(self, df):
            return 2 * df[self._col]
    
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
    
        sep_child = SepChild
        
        class SepChildB(SepChild):
            _col = SourceCols.b

.. code:: ipython3

    df = pd.DataFrame({
        SourceCols.x: [1.5, 3.4, 9.1], SourceCols.b: [False, True, True]
    }).pipe(Cols())

.. code:: ipython3

    df.T




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>x</th>
          <td>1.5</td>
          <td>3.4</td>
          <td>9.1</td>
        </tr>
        <tr>
          <th>b</th>
          <td>False</td>
          <td>True</td>
          <td>True</td>
        </tr>
        <tr>
          <th>col_one</th>
          <td>1</td>
          <td>1</td>
          <td>1</td>
        </tr>
        <tr>
          <th>sub_col__fing</th>
          <td>2.5</td>
          <td>5.4</td>
          <td>11.1</td>
        </tr>
        <tr>
          <th>sub_col__sub_sub_col__sub_x</th>
          <td>0</td>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>sub_col__sub_sub_col__sub_y</th>
          <td>pref_1</td>
          <td>pref_1</td>
          <td>pref_1</td>
        </tr>
        <tr>
          <th>sub_col__sub_sub_col_2__sub_x</th>
          <td>0</td>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>sub_col__sub_sub_col_2__sub_y</th>
          <td>pref2_1</td>
          <td>pref2_1</td>
          <td>pref2_1</td>
        </tr>
        <tr>
          <th>sep_child__neg</th>
          <td>-1.5</td>
          <td>-3.4</td>
          <td>-9.1</td>
        </tr>
        <tr>
          <th>sep_child__double</th>
          <td>3.0</td>
          <td>6.8</td>
          <td>18.2</td>
        </tr>
        <tr>
          <th>sep_child_b__neg</th>
          <td>True</td>
          <td>False</td>
          <td>False</td>
        </tr>
        <tr>
          <th>sep_child_b__double</th>
          <td>0</td>
          <td>2</td>
          <td>2</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    df.loc[:, [Cols.sep_child.double, Cols.SubCol.SubSubCol2.sub_x]]




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>sep_child__double</th>
          <th>sub_col__sub_sub_col_2__sub_x</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>3.0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>6.8</td>
          <td>0</td>
        </tr>
        <tr>
          <th>2</th>
          <td>18.2</td>
          <td>0</td>
        </tr>
      </tbody>
    </table>
    </div>



Designated Child Assigner
-------------------------

   These are designed for information sharing among assigners and **do
   not** take the dataframe as arguments for their methods but, take
   both the df and their parent assigner as parameters for their
   ``__init__``

.. code:: ipython3

    import numpy as np
    
    from colassigner import ChildColAssigner

.. code:: ipython3

    class RawCols(ColAccessor):
        
        cat = str
        num = int
    
    class RawCols2(ColAccessor):
        b = str
        c = str
    
    class IntSides(ChildColAssigner):
        
        # note the type and order of the parameters:
        def __init__(self, df, parent_assigner: "GbReindex") -> None:
            self.arr = parent_assigner.arr
    
        # note the absence of parameters
        def lower(self):
            return np.floor(self.arr).astype(int)
    
        def upper(self):
            return np.ceil(self.arr).astype(int)
    
    class GbReindex(ChildColAssigner):
        main_col = ...
    
        def __init__(self, df, bc: "BaseCols"):
            # note that this reindex needs to be done only once
            # and can be used in many child assigners
            self.arr = bc.base_gb.reindex(df[self.main_col]).values
    
        def values(self):
            return self.arr
    
        sides = IntSides
    
    class BaseCols(ColAssigner):
        def __init__(self, base_df):
            self.base_gb = base_df.groupby(RawCols.cat)[RawCols.num].mean()
    
        class GbB(GbReindex):
            main_col = RawCols2.b
    
        class GbC(GbReindex):
            main_col = RawCols2.c
    
        def prod(self, df):
            return df.loc[
                :, [BaseCols.GbB.sides.lower, BaseCols.GbC.values]
            ].prod(axis=1)

.. code:: ipython3

    df1 = pd.DataFrame({RawCols.cat: ["x", "y", "y"], RawCols.num: [2, 3, 4]})

.. code:: ipython3

    assigner = BaseCols(df1)

.. code:: ipython3

    df2 = pd.DataFrame({"b": ["x", "y", "x"], "c": ["y", "y", "x"]}).pipe(assigner)

.. code:: ipython3

    df2




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>b</th>
          <th>c</th>
          <th>gb_b__values</th>
          <th>gb_b__sides__lower</th>
          <th>gb_b__sides__upper</th>
          <th>gb_c__values</th>
          <th>gb_c__sides__lower</th>
          <th>gb_c__sides__upper</th>
          <th>prod</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>x</td>
          <td>y</td>
          <td>2.0</td>
          <td>2</td>
          <td>2</td>
          <td>3.5</td>
          <td>3</td>
          <td>4</td>
          <td>7.0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>y</td>
          <td>y</td>
          <td>3.5</td>
          <td>3</td>
          <td>4</td>
          <td>3.5</td>
          <td>3</td>
          <td>4</td>
          <td>10.5</td>
        </tr>
        <tr>
          <th>2</th>
          <td>x</td>
          <td>x</td>
          <td>2.0</td>
          <td>2</td>
          <td>2</td>
          <td>2.0</td>
          <td>2</td>
          <td>2</td>
          <td>4.0</td>
        </tr>
      </tbody>
    </table>
    </div>


