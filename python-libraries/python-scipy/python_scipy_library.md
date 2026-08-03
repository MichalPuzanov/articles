# Python SciPy Library
SciPy (Scientific Python) is a free and open-source Python library for scientific, mathematical, and technical computing. It provides a broad collection of high-level numerical algorithms and utility functions designed to support complex computation efficiently.

This notebook offers an introductory overview of SciPy and aims to provide foundational orientation for learners who are beginning to use the library.

SciPy is widely used in both academic research and industry. It is applied by data scientists, machine learning engineers, financial analysts, physicists, and mechanical and electrical engineers to model real-world systems and analyse empirical data.

## Key Characteristics
- **Built on NumPy:** SciPy is constructed directly on top of NumPy and uses NumPy arrays as its core data structure.
- **High Performance:** Although SciPy is used through Python, many core algorithms are implemented in optimised low-level languages such as C, C++, and Fortran.
- **Core Ecosystem Component:** SciPy forms a central part of the scientific Python ecosystem and integrates naturally with libraries such as pandas, Matplotlib, and scikit-learn.

## Core Features and Capabilities
SciPy is organised into specialised subpackages, each addressing a specific mathematical or engineering domain. Major subpackages include:
- **scipy.optimize:** Function minimisation and maximisation, curve fitting, and root finding.
- **scipy.integrate:** Numerical integration and ordinary differential equation (ODE) solvers.
- **scipy.stats:** Probability distributions, descriptive statistics, and hypothesis testing (for example, t-tests).
- **scipy.linalg:** Advanced linear algebra, including matrix decompositions (LU, QR, SVD) and eigenvalue solvers.
- **scipy.signal** and **scipy.fft:** Digital signal processing, filtering, convolution, and Fast Fourier Transform methods.
- **scipy.interpolate:** Estimation of intermediate values between known data points, including spline and linear interpolation.
- **scipy.sparse:** Memory-efficient sparse matrix structures and related solvers.

## SciPy vs NumPy

- **Core focus:** 
    - NumPy - array data structures and fundamental array operations.
    - SciPy - advanced scientific and engineering algorithms.
- **Functionality:**
    - NumPy - indexing, sorting, reshaping, and basic linear algebra.
    - SciPy - optimalisation, signal processing, integration, and statistical analysis
- **Relatioship:**
    - NumPy - fondational library
    - SciPy - built directly on top of NumPy

## Practical Examples
### Installation
*Using pip*
<pre>pip install scipy
</pre>
*Using conda*
<pre>conda install scipy
</pre>
*Using poetry*
<pre>poetry add scipy
</pre>

### Verifying the Installation


```python
from scipy import __version__ as scipy_version

# Check SciPy version
print(f"SciPy version: {scipy_version}")
```

    SciPy version: 1.18.0


### Constants and Special Functions


```python
from scipy import constants, special
```

*Mathematical and Physical Constants*


```python
print("Pi:", constants.pi)
print("Golden ratio:", constants.golden_ratio)
print("Speed of light (m/s):", constants.speed_of_light)
```

    Pi: 3.141592653589793
    Golden ratio: 1.618033988749895
    Speed of light (m/s): 299792458.0


*Representative Special Functions*


```python
print("Factorial(5):", special.factorial(5))
print("Combinations C(6, 2):", special.comb(6, 2))
print("Gamma(5):", special.gamma(5))
print("Bessel J0 at x=1:", special.jv(0, 1.0))
print("Error function erf(1):", special.erf(1.0))
```

    Factorial(5): 120.0
    Combinations C(6, 2): 15.0
    Gamma(5): 24.0
    Bessel J0 at x=1: 0.7651976865579666
    Error function erf(1): 0.8427007929497148


### Linear abgebra


```python
from scipy import linalg
import numpy as np

a = np.array([[3.0, 2.0], [1.0, 4.0]])
b = np.array([[7.0], [5.0]])
```

*Solving Linear Systems*


```python
solution = linalg.solve(a, b)

print("Solution of the linear system Ax = b:")
print(solution)
```

    Solution of the linear system Ax = b:
    [[1.8]
     [0.8]]


*Matrix Properties*


```python
print("Determinant of matrix a:", linalg.det(a))
print("Inverse of matrix a:")
print(linalg.inv(a))
```

    Determinant of matrix a: 10.0
    Inverse of matrix a:
    [[ 0.4 -0.2]
     [-0.1  0.3]]


*Matrix Decompositions*


```python
p, l, u = linalg.lu(a)

print("LU decomposition of matrix a:")
print("P matrix:")
print(p)
print("\nL matrix:")
print(l)
print("\nU matrix:")
print(u)

u_matrix, s, vh = linalg.svd(a)

print("\nSingular Value Decomposition of matrix a:")
print("U matrix:")
print(u_matrix)
print("\nSingular values:")
print(s)
print("\nV^H matrix:")
print(vh)
```

    LU decomposition of matrix a:
    P matrix:
    [[1. 0.]
     [0. 1.]]
    
    L matrix:
    [[1.         0.        ]
     [0.33333333 1.        ]]
    
    U matrix:
    [[3.         2.        ]
     [0.         3.33333333]]
    
    Singular Value Decomposition of matrix a:
    U matrix:
    [[-0.64074744 -0.76775173]
     [-0.76775173  0.64074744]]
    
    Singular values:
    [5.11667274 1.95439508]
    
    V^H matrix:
    [[-0.52573111 -0.85065081]
     [-0.85065081  0.52573111]]


### Optimisation


```python
from scipy import optimize

def objective_function(x):
    return (x - 3) ** 2 + 2
```

*Scalar Function Minimisation*


```python
min_result = optimize.minimize_scalar(objective_function)

print("\nOptimisation result:")
print("Optimal x:", min_result.x)
print("Objective function value at optimal x:", round(min_result.fun, 4))
```

    
    Optimisation result:
    Optimal x: 3.0
    Objective function value at optimal x: 2.0


*Root Finding*


```python
root_result = optimize.root_scalar(lambda x: x ** 3 - 2, bracket=[0, 2])

print("Cube root of 2:", round(root_result.root, 6))
```

    Cube root of 2: 1.259921


*Curve Fitting*


```python
x_data = np.array([0, 1, 2, 3, 4], dtype=float)
y_data = np.array([1.1, 2.9, 7.2, 12.8, 21.1], dtype=float)
fit_params, _ = optimize.curve_fit(lambda x, a, b: a * x ** 2 + b, x_data, y_data)

print("Fitted parameters (a, b):", fit_params)
```

    Fitted parameters (a, b): [1.22931034 1.64413793]


### Numerical Integration


```python
from scipy import integrate
```

*Numerical Integration of x^2 from 0 to 1*


```python
integral_result, error_estimate = integrate.quad(lambda x: x ** 2, 0, 1)
print("Definite integral of exp(-x^2) from 0 to 1:")
print("Integral result:", round(integral_result, 6))
print("Error estimate:", error_estimate)
```

    Definite integral of exp(-x^2) from 0 to 1:
    Integral result: 0.333333
    Error estimate: 3.700743415417189e-15


*Trapezoidal Integration for Sampled Data*


```python
x = np.linspace(0, np.pi, 5)
y = np.sin(x)
trap_result = integrate.trapezoid(y, x)

print("Trapezoid result for sin(x):", trap_result)
```

    Trapezoid result for sin(x): 1.8961188979370398


*Solving a Simple ODE: y' = -0.5y*


```python
ode_solution = integrate.solve_ivp(
    lambda t, values: -0.5 * values,
    t_span=(0, 5),
    y0=[2.0],
    t_eval=np.linspace(0, 5, 6),
)

print("ODE t values:", ode_solution.t)
print("ODE y values:", ode_solution.y[0])
```

    ODE t values: [0. 1. 2. 3. 4. 5.]
    ODE y values: [2.         1.21305368 0.73534013 0.44651426 0.2706912  0.16434549]


### Interpolation Methods


```python
from scipy import interpolate

x = np.array([0, 1, 2, 3, 4], dtype=float)
y = np.array([0, 1, 4, 9, 16], dtype=float)
x_new = np.linspace(0, 4, 10)
```

*Piecewise Interpolation*


```python
linear_interp = interpolate.interp1d(x, y)
cubic_interp = interpolate.interp1d(x, y, kind='cubic')

print("Linear interpolation:", linear_interp(x_new))
print("Cubic interpolation:", cubic_interp(x_new))
```

    Linear interpolation: [ 0.          0.44444444  0.88888889  2.          3.33333333  5.11111111
      7.33333333  9.77777778 12.88888889 16.        ]
    Cubic interpolation: [ 0.          0.19753086  0.79012346  1.77777778  3.16049383  4.9382716
      7.11111111  9.67901235 12.64197531 16.        ]


*Cubic Spline Interpolation*


```python
spline = interpolate.CubicSpline(x, y)

print("Spline value at x=2.5:", spline(2.5))
```

    Spline value at x=2.5: 6.25


### Statistical Analysis


```python
from scipy import stats

sample = np.array([1.2, 2.3, 2.9, 3.5, 4.1, 5.0, 5.8, 6.2, 7.1, 8.0])
```

*Descriptive Statistics*


```python
description = stats.describe(sample)

print("count:", description.nobs)
print("min:", description.minmax[0])
print("max:", description.minmax[1])
print("mean:", description.mean)
print("variance:", description.variance)

```

    count: 10
    min: 1.2
    max: 8.0
    mean: 4.61
    variance: 4.796555555555555


*Hypothesis Testing*


```python
t_stat, p_value = stats.ttest_1samp(sample, popmean=5.0)

print("One-sample t-test:", (t_stat, p_value))
```

    One-sample t-test: (np.float64(-0.5631185935851243), np.float64(0.5871066468209352))


*Probability Distribution Utilities*


```python
print("Normal CDF at 1.96:", stats.norm.cdf(1.96))
print("95th percentile of normal distribution:", stats.norm.ppf(0.95))
```

    Normal CDF at 1.96: 0.9750021048517795
    95th percentile of normal distribution: 1.6448536269514722


*Correlation Analysis*


```python
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])

correlation, corr_p_value = stats.pearsonr(x, y)

print("Pearson correlation:", correlation)
print("Correlation p-value:", corr_p_value)
```

    Pearson correlation: 0.7745966692414834
    Correlation p-value: 0.1240270626575546


### Fast Fourier Transform (FFT)


```python
from scipy import fft

time_step = 0.1
wave = np.array([0, 1, 0, -1, 0, 1, 0, -1], dtype=float)
```

*Forward FFT*


```python
frequency_domain = fft.fft(wave)
frequencies = fft.fftfreq(wave.size, d=time_step)

print("Frequencies:", frequencies)
print("FFT coefficients:", np.round(frequency_domain, 3))
```

    Frequencies: [ 0.    1.25  2.5   3.75 -5.   -3.75 -2.5  -1.25]
    FFT coefficients: [0.-0.j 0.+0.j 0.-4.j 0.+0.j 0.-0.j 0.-0.j 0.+4.j 0.-0.j]


*Inverse FFT*


```python
reconstructed = fft.ifft(frequency_domain)

print("Recovered signal:", reconstructed.real)
```

    Recovered signal: [ 0.  1.  0. -1.  0.  1.  0. -1.]


### Signal Processing


```python
from scipy import signal

time = np.linspace(0, 1, 200, endpoint=False)
waveform = np.sin(2 * np.pi * 5 * time) + 0.5 * np.sin(2 * np.pi * 20 * time)
```

*Low-pass Butterworth Filtering*


```python
b, a = signal.butter(4, 0.15)
filtered = signal.filtfilt(b, a, waveform)

print("Original first 5 samples:", np.round(waveform[:5], 3))
print("Filtered first 5 samples:", np.round(filtered[:5], 3))
```

    Original first 5 samples: [0.    0.45  0.785 0.93  0.882]
    Filtered first 5 samples: [-0.008  0.175  0.346  0.493  0.614]


*Peak Detection*


```python
peaks, properties = signal.find_peaks(waveform, height=1.0)

print("Peak indices:", peaks[:5])
print("Peak heights:", np.round(properties["peak_heights"][:5], 3))
```

    Peak indices: [ 12  52  92 132 172]
    Peak heights: [1.427 1.427 1.427 1.427 1.427]


*Cross-correlation*


```python
correlation = signal.correlate([1, 2, 3], [0, 1, 0.5], mode="full")
print("\nCross-correlation:", correlation)
```

    
    Cross-correlation: [0.5 2.  3.5 3.  0. ]


### Sparse Matrix Computation


```python
from scipy import sparse

dense = np.array([
    [0, 0, 3, 0],
    [4, 0, 0, 0],
    [0, 0, 5, 7],
    [0, 2, 0, 0],
])
```

*Constructing Sparse Formats*


```python
csr = sparse.csr_matrix(dense)
coo = sparse.coo_matrix(dense)

print("CSR matrix:\n", csr)
print("\nNon-zero count:", csr.nnz)
```

    CSR matrix:
     <Compressed Sparse Row sparse matrix of dtype 'int64'
    	with 5 stored elements and shape (4, 4)>
      Coords	Values
      (0, 2)	3
      (1, 0)	4
      (2, 2)	5
      (2, 3)	7
      (3, 1)	2
    
    Non-zero count: 5


*Sparse Matrix Operations*


```python
vector = np.array([1, 2, 3, 4])

product = csr @ vector
print("Sparse matrix-vector product:", product)

identity = sparse.eye(4, format="csr")
print("Identity sparse matrix:\n", identity.toarray())

```

    Sparse matrix-vector product: [ 9  4 43  4]
    Identity sparse matrix:
     [[1. 0. 0. 0.]
     [0. 1. 0. 0.]
     [0. 0. 1. 0.]
     [0. 0. 0. 1.]]


### Spatial Algorithms


```python
from scipy import spatial

points = np.array([
    [0.0, 0.0],
    [1.0, 1.0],
    [2.0, 0.5],
    [0.5, 2.0],
    [1.5, 1.8],
])
```

*KD-tree Nearest-neighbour Search*


```python
tree = spatial.KDTree(points)
distance, index = tree.query([0.9, 1.1])

print("Nearest point index:", index)
print("Nearest point:", points[index])
print("Distance:", distance)
```

    Nearest point index: 1
    Nearest point: [1. 1.]
    Distance: 0.14142135623730953


*Pairwise Distance Computation*


```python
distance_matrix = spatial.distance.cdist(points[:2], points[2:])

print("Distance matrix:\n", np.round(distance_matrix, 3))
```

    Distance matrix:
     [[2.062 2.062 2.343]
     [1.118 1.118 0.943]]


*Convex Hull Construction*


```python
hull = spatial.ConvexHull(points)

print("Convex hull vertex indices:", hull.vertices)
```

    Convex hull vertex indices: [0 2 4 3]


### Image Processing


```python
from scipy import ndimage

test_image = np.arange(16, dtype=float).reshape(4, 4)
```

*Filtering and Geometric Transforms*


```python
blurred = ndimage.gaussian_filter(test_image, sigma=1.0)
edges = ndimage.sobel(test_image, axis=0)
rotated = ndimage.rotate(test_image, 45, reshape=False)

print("Original image:\n", test_image)
print("\nBlurred image:\n", np.round(blurred, 2))
print("\nVertical Sobel edges:\n", edges)
print("\nRotated image:\n", np.round(rotated, 2))
```

    Original image:
     [[ 0.  1.  2.  3.]
     [ 4.  5.  6.  7.]
     [ 8.  9. 10. 11.]
     [12. 13. 14. 15.]]
    
    Blurred image:
     [[ 2.13  2.77  3.64  4.28]
     [ 4.68  5.32  6.19  6.83]
     [ 8.17  8.81  9.68 10.32]
     [10.72 11.36 12.23 12.87]]
    
    Vertical Sobel edges:
     [[16. 16. 16. 16.]
     [32. 32. 32. 32.]
     [32. 32. 32. 32.]
     [16. 16. 16. 16.]]
    
    Rotated image:
     [[ 0.    2.32  5.92  0.  ]
     [ 0.78  4.43  8.27 12.06]
     [ 2.94  6.73 10.57 14.22]
     [ 0.    9.08 12.68  0.  ]]


*Connected-component Labelling*


```python
mask = np.array([[1, 0, 0], [1, 1, 0], [0, 0, 1]])

labels, num_features = ndimage.label(mask)

print("Labeled components:\n", labels)
print("Number of features:", num_features)
```

    Labeled components:
     [[1 0 0]
     [1 1 0]
     [0 0 2]]
    Number of features: 2


### Clustering Methods


```python
from scipy.cluster import hierarchy, vq

data = np.array([
    [1.0, 1.0],
    [1.2, 0.9],
    [3.0, 3.1],
    [3.2, 2.9],
    [8.0, 8.0],
])
```

*Hierarchical Clustering*


```python
linkage_matrix = hierarchy.linkage(data, method="ward")
cluster_labels = hierarchy.fcluster(linkage_matrix, t=2.5, criterion="distance")

print("Cluster labels from hierarchy:", cluster_labels)
```

    Cluster labels from hierarchy: [1 1 2 2 3]


*K-means-style Vector Quantisation*


```python
centroids, distortion = vq.kmeans(data, 2)
codes, distances = vq.vq(data, centroids)

print("Centroids:\n", np.round(centroids, 3))
print("Distortion:", distortion)
print("Assigned cluster codes:", codes)
print("Distances to centroids:", np.round(distances, 3))
```

    Centroids:
     [[2.1   1.975]
     [8.    8.   ]]
    Distortion: 1.1499690274985555
    Assigned cluster codes: [0 0 0 0 1]
    Distances to centroids: [1.47  1.402 1.441 1.437 0.   ]


## Conclusion
SciPy provides a coherent and mature toolkit for scientific computing in Python, extending NumPy with specialised algorithms for optimisation, integration, interpolation, statistics, signal processing, sparse matrices, spatial analysis, image processing, and clustering. Across the examples in this notebook, a consistent workflow emerges: represent data as arrays, select an appropriate SciPy submodule, and apply high-level numerical routines through clear and reproducible code.

In practical settings, SciPy is most effective when used as part of the broader scientific Python ecosystem. NumPy supports efficient array operations, while libraries such as Matplotlib and pandas complement SciPy through visualisation and structured data analysis. Collectively, these tools support reliable problem solving in research and professional environments where numerical accuracy, computational performance, and maintainability are all essential.

For further study, a productive next step is to select one domain-relevant submodule, for example `scipy.optimize`, `scipy.stats`, or `scipy.signal`, and examine its API in greater depth using real datasets and systematic parameter tuning. This focused approach develops both practical intuition and methodological confidence, helping to translate foundational examples into robust analytical workflows.
