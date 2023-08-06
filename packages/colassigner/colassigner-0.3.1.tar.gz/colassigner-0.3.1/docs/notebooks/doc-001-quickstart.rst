Quickstart
==========

Assign Columns
--------------

.. code:: ipython3

    import pandas as pd
    
    from colassigner import ColAssigner

.. code:: ipython3

    class Cols(ColAssigner):
        def col1(self, df):
            return df.iloc[:, 0] * 2
    
        def col2(self, df):
            return "added-another"

.. code:: ipython3

    df = pd.DataFrame({"a": [1, 2, 3]}).pipe(Cols())

.. code:: ipython3

    df




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
          <th>a</th>
          <th>col_1</th>
          <th>col_2</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>1</td>
          <td>2</td>
          <td>added-another</td>
        </tr>
        <tr>
          <th>1</th>
          <td>2</td>
          <td>4</td>
          <td>added-another</td>
        </tr>
        <tr>
          <th>2</th>
          <td>3</td>
          <td>6</td>
          <td>added-another</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    df.loc[:, Cols.col2]




.. parsed-literal::

    0    added-another
    1    added-another
    2    added-another
    Name: col_2, dtype: object



Access Columns
--------------

while also documenting datatypes

.. code:: ipython3

    from colassigner import ColAccessor

.. code:: ipython3

    class Cols(ColAccessor):
    
        x = int
        y = float

.. code:: ipython3

    df = pd.DataFrame({Cols.x: [1, 2, 3], Cols.y: [0.3, 0.1, 0.9]})

.. code:: ipython3

    df




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
          <th>x</th>
          <th>y</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>1</td>
          <td>0.3</td>
        </tr>
        <tr>
          <th>1</th>
          <td>2</td>
          <td>0.1</td>
        </tr>
        <tr>
          <th>2</th>
          <td>3</td>
          <td>0.9</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    df.loc[:, Cols.y]




.. parsed-literal::

    0    0.3
    1    0.1
    2    0.9
    Name: y, dtype: float64


