# Specs of NN translator object

The NN translator should take a file containing the empirical formula and an
array containing all the 1H NMR spectral data. NN translator expects this file
to be constructed as:
```
empirical formula: <xxx>
Peak Location, Peak area, Peak Multiplicity
<xxx>,<xxx>,<xxx>
...
...
Connectivity matrix
x_11,...,x_1n
...
x_n1,....,x_nn
```

The connectivity matrix is optional, based on whether or not it is a training
file.

Inputs:
 * Filename of input file
 * Boolean of whether it is a training file. (default is `False`)
Output:
 * Tuple containing:
   1.  Vector containing the empirical formula and linspace of spectral data in
   		the following format:
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
		 ...
		 <ppm 0.00 area>
		 <ppm 0.00 mult>
		 <ppm 0.01 area>
		 <ppm 0.01 mult>
		 <ppm 0.02 area>
		 <ppm 0.02 mult>
		 <ppm 0.03 area>
		 <ppm 0.03 mult>
		 <ppm 0.04 area>
		 <ppm 0.04 mult>
		 ...
		 <ppm (max) area>
		 <ppm (max) mult>]
		 ```
   2. Connectivity matrix in NN output space. Should be of size `(nmaxatoms,
	  nmaxatoms)`. `None` if testing is `False`.

Errors thrown:
 * On a non-string for filename, `TypeError`
 * On a non-bool for testing, `TypeError`
 * On a nonexistent file, `FileNotFoundError`
 * On a file with improper format, `ValueError`
