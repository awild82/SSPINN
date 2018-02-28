The expected input for the neural net is:
```
 [<# of H>,
 <# of C>,
 <# of N>,
 <# of O>,
 <# of F>,
 <# of Cl>,
 <# of Br>,
 <# of I>,
 <# of P>,
 <# of B>,
 <# of S>,
 <ppm 0.0 mult>
 <ppm 0.1 mult>
 <ppm 0.2 mult>
 <ppm 0.3 mult>
 <ppm 0.4 mult>
 ...
 <ppm 333.8  mult>]
```

An example for this, with the empirical formula C3H8O, a singlet at 17.1 ppm,
and a triplet at 18.3 ppm, (Yeah, I know that doesn't make physical sense -
it's just an example) would look like:

```
 [8,
  3,
  0,
  1,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  ... (zeros until 17.1)
  1,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  3,
  ... (zeros until the end)
  0]
```


