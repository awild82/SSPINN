The output of the neural net will be an unraveled 432 by 432 connectivity
matrix. The columns and rows are grouped by atom. The maximum number of each
atom is given below.

* C: 144
* O: 39
* H: 183
* N: 19
* S: 8
* F: 12
* Cl: 10
* Br: 6
* P: 2
* I: 6
* B: 3

The matrix should be organized in the same order as the empirical formula in
the input:
```
 <H rows>
 <C rows>
 <N rows>
 <O rows>
 <F rows>
 <Cl rows>
 <Br rows>
 <I rows>
 <P rows>
 <B rows>
 <S rows>
````

The predictor will do the unraveling. The nn_translator ought to provide the
matrix, not the unraveled vector.
