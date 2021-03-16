# CSP-error-LinAlgError

I face the following error when running the CSP function of the MNE package using the EEG BCI dataset:

LinAlgError : The leading minor of order 64 of B is not positive definite. The factorization of B could not be completed and no eigenvalues or eigenvectors were computed.

In this repository I first save a compressed .npz file with data raising the error (savedataforexample.py) and tehn include a minimalscript.py file to raise the error by loading the data
and calling the CSP function. 
