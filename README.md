# CSP-error-LinAlgError

I face the following error when running the CSP function of the MNE package using the EEG BCI dataset:

LinAlgError : The leading minor of order 64 of B is not positive definite. The factorization of B could not be completed and no eigenvalues or eigenvectors were computed.

In this repository I first save a compressed .npz file with data raising the error (savedataforexample.py) and tehn include a minimalscript.py file to raise the error by loading the data
and calling the CSP function. 

More info:

- the provided data are from subject[2] from the EEG BCI dataset; the error sometimes occurs with other subjects, sometimes not
- changing reg parameter (1e-4, 1e-10, 'oas') does not help
- leaving out ICA sometimes helps (ICA is performed on provided data)
- post-mortem debugging: np.linalg.svd(x)[1][[0, -1]] --> [5.14015052e-09 1.12520815e-24]
- script of preprocessing steps shown here: https://mne.discourse.group/t/csp-error-linalgerror-the-leading-minor-of-order-64-of-b-is-not-positive-definite/2755
- mne.sys_info()
Platform:      Windows-10-10.0.19041-SP0
Python:        3.8.3 (default, Jul  2 2020, 17:30:36) [MSC v.1916 64 bit (AMD64)]
Executable:    C:\Users\????\Anaconda3\python.exe
CPU:           Intel64 Family 6 Model 142 Stepping 10, GenuineIntel: 8 cores
Memory:        7.9 GB

mne:           0.22.0
numpy:         1.18.5 {blas=mkl_rt, lapack=mkl_rt}
scipy:         1.5.4
matplotlib:    3.3.3 {backend=module://ipykernel.pylab.backend_inline}

sklearn:       0.23.2
numba:         0.50.1
nibabel:       Not found
nilearn:       Not found
dipy:          Not found
cupy:          Not found
pandas:        1.0.5
mayavi:        Not found
pyvista:       Not found
vtk:           Not found
