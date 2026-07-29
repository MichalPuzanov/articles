# Python NumPy Library

NumPy (Numerical Python) is a foundational open-source Python library for numerical and mathematical computation.

It introduces the N-dimensional array (`ndarray`), a high-performance data structure for storing and manipulating large datasets efficiently. NumPy forms the computational foundation of the Python data-science ecosystem; major libraries such as Pandas, SciPy, scikit-learn, and TensorFlow build directly upon it.

This tutorial is designed to provide a concise yet practical overview of NumPy and to support day-to-day technical work through clear, task-oriented examples.

## Key characteristics
- **High performance:** NumPy operations are implemented in highly optimised C, enabling many numerical workloads to run substantially faster than equivalent operations on standard Python lists.
- **Vectorisation:** NumPy reduces reliance on explicit Python loops by applying operations across entire arrays in a single expression.
- **Memory efficiency:** NumPy arrays store homogeneous data in contiguous memory blocks, typically reducing memory overhead relative to Python lists.

## Core features and capabilities
NumPy provides a broad suite of tools for numerical computation, including:

- **Multidimensional arrays:** Creation and manipulation of 1D vectors, 2D matrices, and higher-dimensional structures.
- **Broadcasting:** Arithmetic operations between arrays of different, but compatible, shapes.
- **Linear algebra:** Built-in routines for matrix multiplication, determinants, inverses, and systems of linear equations.
- **Random number generation:** Utilities for generating random samples from common statistical distributions.
- **Mathematical functions:** Fast element-wise operations for trigonometric, logarithmic, exponential, and statistical calculations (for example, mean, median, and standard deviation).

## Python lists vs NumPy ndarrays
- **Python lists** can store heterogeneous data types (for example, strings, integers, and objects) in a single container. This flexibility is useful, but lists are comparatively inefficient for numerical computation.
- **NumPy ndarrays** are homogeneous (all elements share the same data type). This design supports efficient vectorised operations and improved memory efficiency.

## Practical examples

### Installation
*Using pip*
<pre>pip install numpy
</pre>

*Using conda*
<pre>conda install numpy
</pre>

*Using poetry*
<pre>poetry add numpy
</pre>

### Verify the installation
The following test script can be used to confirm that NumPy has been installed correctly.


```python
import numpy as np

# Check NumPy version
print(f"NumPy version: {np.__version__}")
```

    NumPy version: 2.5.1


### `Ndarray` creation
This section demonstrates several standard methods for creating NumPy arrays.

*One-dimensional ndarray*


```python
arr1d = np.array([1, 2, 3, 4, 5])
print("From list:", arr1d)
```

    From list: [1 2 3 4 5]


*Two-dimensional ndarray*


```python
arr2d= np.array([[1, 2, 3], [4, 5, 6]])
print("\n2D array:\n", arr2d)
```

    
    2D array:
     [[1 2 3]
     [4 5 6]]


*Zero-filled and one-filled arrays*


```python
zeros = np.zeros(5)
print("\nZeros:", zeros)

ones = np.ones((3, 3))
print("\nOnes:\n", ones)
```

    
    Zeros: [0. 0. 0. 0. 0.]
    
    Ones:
     [[1. 1. 1.]
     [1. 1. 1.]
     [1. 1. 1.]]


*Range-based and evenly spaced sequences*


```python
range_arr = np.arange(0, 10, 2)
print("\nRange (0 to 10, step 2):", range_arr)

linspace_arr = np.linspace(0, 10, 5)
print("\nLinspace (0 to 10, 5 points):", linspace_arr)
```

    
    Range (0 to 10, step 2): [0 2 4 6 8]
    
    Linspace (0 to 10, 5 points): [ 0.   2.5  5.   7.5 10. ]


*Identity and uninitialised arrays*


```python
# create 2D identity matrix
identity = np.eye(3)
print("\nIdentity matrix:\n", identity)

# create 2D array with random garbage values, it is faster than random.rand() and random.randn()
empty = np.empty((2, 2))
print("\nEmpty array shape:", empty.shape)
```

    
    Identity matrix:
     [[1. 0. 0.]
     [0. 1. 0.]
     [0. 0. 1.]]
    
    Empty array shape: (2, 2)


*Randomly generated arrays*


```python
# create 2D array with random values between 0 and 1
random_arr = np.random.rand(3, 3)
print("\nRandom array (0-1):\n", random_arr)

# create 2D array with random integers between 1 and 10
random_int = np.random.randint(1, 10, size=(2, 3))
print("\nRandom integers (1-10):\n", random_int)
```

    
    Random array (0-1):
     [[0.55874991 0.81386435 0.31782834]
     [0.39704509 0.89016825 0.82541621]
     [0.10668708 0.15977588 0.65121931]]
    
    Random integers (1-10):
     [[2 2 9]
     [8 4 4]]


### `Ndarray` properties and attributes
*Reference array*


```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
```

*Array properties*


```python
print("Shape:", arr.shape)
print("Dimensions:", arr.ndim)
print("Size (total elements):", arr.size)
print("Data type:", arr.dtype)
print("Item size (bytes):", arr.itemsize)
print("Strides:", arr.strides)
```

    Shape: (2, 3)
    Dimensions: 2
    Size (total elements): 6
    Data type: int64
    Item size (bytes): 8
    Strides: (24, 8)


*Reshaping arrays*


```python
reshaped = arr.reshape(3, 2)
print("\nReshaped to (3, 2):\n", reshaped)
```

    
    Reshaped to (3, 2):
     [[1 2]
     [3 4]
     [5 6]]


*Flattening arrays*


```python
flattened = arr.flatten()
print("\nFlattened:", flattened)
```

    
    Flattened: [1 2 3 4 5 6]


*Copy versus view*


```python
arr_copy = arr.copy()
arr_view = arr.view()
arr_copy[0, 0] = 999
print("\nOriginal:", arr[0, 0])
print("Copy modified:", arr_copy[0, 0])
arr_view[0, 0] = 888
print("Original after view modified:", arr[0, 0])
print("View modified:", arr_view[0, 0])
```

    
    Original: 1
    Copy modified: 999
    Original after view modified: 888
    View modified: 888


A view is typically faster than creating a copy, but it shares underlying data with the original ndarray. Consequently, modifying values through a view also modifies the original array. Views are particularly useful when adjusting shape or data-type representations without duplicating data.

*Changing the shape of a view*


```python
# 1. Create a flat 1D original array
original = np.array([10, 20, 30, 40, 50, 60])

# 2. Create a view and change its dimensions to a 2x3 matrix
matrix_view = original.reshape(2, 3)

# 3. Check the shapes
print("Original Shape:", original.shape)
print("View Shape:    ", matrix_view.shape)
print("\nOriginal Array:\n", original)
print("\nMatrix View:\n", matrix_view)
```

    Original Shape: (6,)
    View Shape:     (2, 3)
    
    Original Array:
     [10 20 30 40 50 60]
    
    Matrix View:
     [[10 20 30]
     [40 50 60]]


*Changing the data type representation of a view*


```python
# 1. Create a flat 1D original array
original = np.array([10, 20, 30, 40, 50, 60])

# 2. View the exact same memory bytes as 16-bit integers
# Because 16-bit is half the size of 64-bit, each number splits into four!
matrix_view = original.view(np.int16)

# 3. Check the shapes
print("Original dtype:", original.dtype)
print("View dtype:    ", matrix_view.dtype)
print("\nOriginal Array:\n", original)
print("\nMatrix View:\n", matrix_view)
```

    Original dtype: int64
    View dtype:     int16
    
    Original Array:
     [10 20 30 40 50 60]
    
    Matrix View:
     [10  0  0  0 20  0  0  0 30  0  0  0 40  0  0  0 50  0  0  0 60  0  0  0]


### Indexing, slicing, and `where` conditions

*Reference arrays*


```python
arr = np.arange(20)
arr_2d = np.arange(24).reshape(4, 6)

print("Original 1D:", arr)
print("\n2D array:\n", arr_2d)
```

    Original 1D: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19]
    
    2D array:
     [[ 0  1  2  3  4  5]
     [ 6  7  8  9 10 11]
     [12 13 14 15 16 17]
     [18 19 20 21 22 23]]


*Basic indexing*


```python
print("\nElement at index 5:", arr[5])
print("Element at [0, 2]:", arr_2d[0, 2])
print("First row:", arr_2d[0])
print("Last column:", arr_2d[:, -1])
```

    
    Element at index 5: 5
    Element at [0, 2]: 2
    First row: [0 1 2 3 4 5]
    Last column: [ 5 11 17 23]


*Boolean indexing*


```python
mask = (arr > 10) & (arr < 15)
print("\nArr > 10 and < 15:", arr[mask])
```

    
    Arr > 10 and < 15: [11 12 13 14]


*Fancy indexing through explicit index selection*


```python
indices = [0, 5, 10, 15]
print("arr[[0, 5, 10, 15]]:", arr[indices])
```

    arr[[0, 5, 10, 15]]: [ 0  5 10 15]


*Slicing operations*


```python
print("\narr[5:10]:", arr[5:10])
print("arr[::2]:", arr[::2])  # Every 2nd element
print("arr[::-1]:", arr[::-1])  # Reversed
```

    
    arr[5:10]: [5 6 7 8 9]
    arr[::2]: [ 0  2  4  6  8 10 12 14 16 18]
    arr[::-1]: [19 18 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0]


*Two-dimensional slicing*


```python
print("\narr_2d[1:3, 2:5]:\n", arr_2d[1:3, 2:5])
print("\narr_2d[:, 1]:", arr_2d[:, 1])  # All rows, column 1
```

    
    arr_2d[1:3, 2:5]:
     [[ 8  9 10]
     [14 15 16]]
    
    arr_2d[:, 1]: [ 1  7 13 19]


*Conditional selection with `where`*


```python
result = np.where(arr > 10, arr, 0)
print("\nWhere arr > 10:", result)
```

    
    Where arr > 10: [ 0  0  0  0  0  0  0  0  0  0  0 11 12 13 14 15 16 17 18 19]


### Arithmetic and mathematical operations
Unlike Python lists, NumPy applies operations across entire ndarrays.

*Reference arrays*


```python
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])
```

*Basic arithmetic operations*


```python
print("a + b:", a + b)
print("a - b:", a - b)
print("a * b:", a * b)
print("b / a:", b / a)
print("a ** 2:", a ** 2)
```

    a + b: [11 22 33 44 55]
    a - b: [ -9 -18 -27 -36 -45]
    a * b: [ 10  40  90 160 250]
    b / a: [10. 10. 10. 10. 10.]
    a ** 2: [ 1  4  9 16 25]


*Universal functions*


```python
print("\nSquare root:", np.sqrt(a))
print("Absolute value:", np.abs(np.array([-1, -2, 3])))
print("Exponential:", np.exp(np.array([1, 2, 3])))
print("Logarithm:", np.log(np.array([1, 2.718, 10])))
```

    
    Square root: [1.         1.41421356 1.73205081 2.         2.23606798]
    Absolute value: [1 2 3]
    Exponential: [ 2.71828183  7.3890561  20.08553692]
    Logarithm: [0.         0.99989632 2.30258509]


*Trigonometric functions*


```python
angles = np.array([0, np.pi/4, np.pi/2, np.pi])

print("\nSine:", np.sin(angles))
print("Cosine:", np.cos(angles))
print("Tangent:", np.tan(angles))
```

    
    Sine: [0.00000000e+00 7.07106781e-01 1.00000000e+00 1.22464680e-16]
    Cosine: [ 1.00000000e+00  7.07106781e-01  6.12323400e-17 -1.00000000e+00]
    Tangent: [ 0.00000000e+00  1.00000000e+00  1.63312394e+16 -1.22464680e-16]


*Rounding functions*


```python
decimals = np.array([1.234, 5.678, 2.567])

print("\nCeiling:", np.ceil(decimals))
print("Floor:", np.floor(decimals))
print("Round:", np.round(decimals, 2))
```

    
    Ceiling: [2. 6. 3.]
    Floor: [1. 5. 2.]
    Round: [1.23 5.68 2.57]


### Statistical functions

*Reference arrays*


```python
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
arr_2d = np.arange(1, 13).reshape(3, 4)
```

*Basic descriptive statistics*


```python
print("Sum:", np.sum(arr))
print("Mean:", np.mean(arr))
print("Median:", np.median(arr))
print("Std Dev:", np.std(arr))
print("Variance:", np.var(arr))
```

    Sum: 55
    Mean: 5.5
    Median: 5.5
    Std Dev: 2.8722813232690143
    Variance: 8.25


*Axis-wise statistics (2D example)*


```python
print("\n2D array:\n", arr_2d)
print("\nSum along axis 0 (columns):", np.sum(arr_2d, axis=0))
print("Sum along axis 1 (rows):", np.sum(arr_2d, axis=1))
print("Mean along axis 0:", np.mean(arr_2d, axis=0))
print("Mean along axis 1:", np.mean(arr_2d, axis=1))
```

    
    2D array:
     [[ 1  2  3  4]
     [ 5  6  7  8]
     [ 9 10 11 12]]
    
    Sum along axis 0 (columns): [15 18 21 24]
    Sum along axis 1 (rows): [10 26 42]
    Mean along axis 0: [5. 6. 7. 8.]
    Mean along axis 1: [ 2.5  6.5 10.5]


*Minimum and maximum functions*


```python
print("\nMin:", np.min(arr))
print("Max:", np.max(arr))
print("Argmin (index):", np.argmin(arr))
print("Argmax (index):", np.argmax(arr))
```

    
    Min: 1
    Max: 10
    Argmin (index): 0
    Argmax (index): 9


*Percentiles*


```python
print("\n25th percentile:", np.percentile(arr, 25))
print("50th percentile (median):", np.percentile(arr, 50))
print("75th percentile:", np.percentile(arr, 75))
```

    
    25th percentile: 3.25
    50th percentile (median): 5.5
    75th percentile: 7.75


*Cumulative operations*


```python
print("\nCumulative sum:", np.cumsum(arr[:5]))
print("Cumulative product:", np.cumprod(np.array([1, 2, 3, 4])))
print("Cumulative max:", np.maximum.accumulate(np.array([1, 3, 2, 5, 4])))
```

    
    Cumulative sum: [ 1  3  6 10 15]
    Cumulative product: [ 1  2  6 24]
    Cumulative max: [1 3 3 5 5]


### Array manipulation

*Reference arrays*


```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
c = np.array([[6, 7, 8, ], [9, 10, 11]])
```

*Concatenation*


```python
concat = np.concatenate([a, b])
print("Concatenate:", concat)
```

    Concatenate: [1 2 3 4 5 6]


*`stack`, `hstack`, and `vstack`*


```python
stacked = np.stack([a, b])
print("\nStack:\n", stacked)

# horizontal
hstacked = np.hstack([a, b])
print("\nHStack:", hstacked)

# vertical
vstacked = np.vstack([[a], [b]])
print("\nVStack:\n", vstacked)
```

    
    Stack:
     [[1 2 3]
     [4 5 6]]
    
    HStack: [1 2 3 4 5 6]
    
    VStack:
     [[1 2 3]
     [4 5 6]]


*Splitting arrays*


```python
arr = np.arange(10)
split_result = np.array_split(arr, 3)
print("\nArray_split into 3 parts:")
for i, part in enumerate(split_result):
    print(f"  Part {i}: {part}")
```

    
    Array_split into 3 parts:
      Part 0: [0 1 2 3]
      Part 1: [4 5 6]
      Part 2: [7 8 9]


*Transposition*


```python
print("\nOriginal:\n", c)
print("Transposed:\n", c.T)
```

    
    Original:
     [[ 6  7  8]
     [ 9 10 11]]
    Transposed:
     [[ 6  9]
     [ 7 10]
     [ 8 11]]


*Unique values*


```python
arr_with_dupes = np.array([1, 2, 2, 3, 3, 3, 4])
print("\nUnique values:", np.unique(arr_with_dupes))
```

    
    Unique values: [1 2 3 4]


*Sorting*


```python
arr_unsorted = np.array([3, 1, 4, 1, 5, 9, 2, 6])
print("Sorted:", np.sort(arr_unsorted))
print("Argsort (indices):", np.argsort(arr_unsorted))
```

    Sorted: [1 1 2 3 4 5 6 9]
    Argsort (indices): [1 3 6 0 2 4 7 5]


### Linear algebra

*Dot product and matrix multiplication*


```python
# 1d ndarrays
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

dot_product = np.dot(a, b)
print("Dot product:", dot_product)  # 1*4 + 2*5 + 3*6 = 32

# 2d ndarrays
mat_a = np.array([[1, 5], [3, 4]])
mat_b = np.array([[5, 6], [7, 8]])

matrix_product = np.dot(mat_a, mat_b)
print("\nMatrix product:\n", matrix_product)

# Using the @ operator for matrix multiplication
matrix_product_operator = mat_a @ mat_b
print("\nMatrix product using @ operator:\n", matrix_product_operator)
```

    Dot product: 32
    
    Matrix product:
     [[40 46]
     [43 50]]
    
    Matrix product using @ operator:
     [[40 46]
     [43 50]]


*Trace (sum of diagonal elements)*


```python
print("Trace:", np.trace(mat_a))
```

    Trace: 5


*`linalg`: linear algebra submodule*


```python
# Determinant
det = np.linalg.det(mat_a)
print("\nDeterminant:", det)

# Inverse
inv = np.linalg.inv(mat_a)
print("\nInverse:\n", inv)

# Eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(mat_a)
print("\nEigenvalues:", eigenvalues)
print("Eigenvectors:\n", eigenvectors)

# Rank
print("\nRank:", np.linalg.matrix_rank(mat_a))

# Norm
print("\nNorm (default):", np.linalg.norm(a))
print("Norm (L2):", np.linalg.norm(a, ord=2))
print("Norm (L1):", np.linalg.norm(a, ord=1))
```

    
    Determinant: -11.000000000000002
    
    Inverse:
     [[-0.36363636  0.45454545]
     [ 0.27272727 -0.09090909]]
    
    Eigenvalues: [-1.65331193+0.j  6.65331193+0.j]
    Eigenvectors:
     [[-0.88333068+0.j -0.66249905+0.j]
     [ 0.46875037+0.j -0.74906275+0.j]]
    
    Rank: 2
    
    Norm (default): 3.7416573867739413
    Norm (L2): 3.7416573867739413
    Norm (L1): 6.0


### Broadcasting
Broadcasting enables operations on ndarrays with different shapes, provided that their dimensions are compatible.

*Array and scalar broadcasting*


```python
arr = np.array([1, 2, 3, 4, 5])
result = arr + 10
print("Array + scalar:", result)
```

    Array + scalar: [11 12 13 14 15]


*One-dimensional and two-dimensional ndarray broadcasting*


```python
arr_1d = np.array([1, 2, 3])
arr_2d = np.array([[10], [20], [30]])

result = arr_1d + arr_2d
print("\n1D + 2D (broadcasting):")
print("Shape (3,) + (3, 1) = (3, 3)")
print(result)
```

    
    1D + 2D (broadcasting):
    Shape (3,) + (3, 1) = (3, 3)
    [[11 12 13]
     [21 22 23]
     [31 32 33]]


*Operations across dimensions*


```python
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
column = np.array([10, 20, 30])

print("\nSubtract column from matrix:")
print(matrix - column)
```

    
    Subtract column from matrix:
    [[ -9 -18 -27]
     [ -6 -15 -24]
     [ -3 -12 -21]]


Broadcasting rules:
1. If arrays have different ranks, pad the smaller shape with leading dimensions of size 1.
2. Check that each aligned dimension is compatible (equal, or one of them is 1).
3. Any dimension of size 1 is conceptually stretched to match the corresponding larger dimension.

*Broadcasting rules: examples*
<pre>Shape (5,) broadcasts with (3, 5) -> (3, 5)
Shape (3, 1) broadcasts with (3, 4) -> (3, 4)
Shape (1, 5) broadcasts with (3, 5) -> (3, 5)
</pre>

### Random number generation

*Set seed for reproducibility*


```python
np.random.seed(1000)  # For reproducibility
```

*Uniform distribution on [0, 1)*


```python
uniform = np.random.rand(5)
print("Uniform [0, 1):", uniform)
```

    Uniform [0, 1): [0.65358959 0.11500694 0.95028286 0.4821914  0.87247454]


*Random integers*


```python
ints = np.random.randint(1, 10, size=5)
print("Random integers [1, 10):", ints)
```

    Random integers [1, 10): [9 5 5 5 3]


*Normal (Gaussian) distribution*


```python
normal = np.random.randn(5)
print("Normal distribution:", normal)
```

    Normal distribution: [ 0.57363145 -0.74841131 -0.4122031  -0.07400906 -0.92893693]


*Normal distribution with custom mean and standard deviation*


```python
custom_normal = np.random.normal(loc=100, scale=15, size=5)
print("\nNormal (μ=100, σ=15):", custom_normal)
```

    
    Normal (μ=100, σ=15): [120.85092205 117.92603993 110.61013587 114.8944316  102.09195908]


*Exponential distribution*


```python
exponential = np.random.exponential(scale=2.0, size=5)
print("Exponential (λ=0.5):", exponential)
```

    Exponential (λ=0.5): [4.69093541 0.02095277 0.1549649  0.56109307 0.28613573]


*Random choice from an ndarray*


```python
arr = np.arange(10)
choices = np.random.choice(arr, size=5, replace=False)
print("\nRandom choice (no replace):", choices)
```

    
    Random choice (no replace): [4 2 8 0 3]


*In-place shuffling*


```python
arr = np.arange(10)
np.random.shuffle(arr)
print("Shuffled:", arr)
```

    Shuffled: [4 9 5 1 3 6 2 0 8 7]


*Shuffling with a copied permutation*


```python
arr = np.arange(10)
shuffled = np.random.permutation(arr)
print("Permutation:", shuffled)
```

    Permutation: [2 8 7 1 4 0 5 6 9 3]


*Binomial distribution*


```python
binomial = np.random.binomial(n=10, p=0.5, size=5)
print("\nBinomial (n=10, p=0.5):", binomial)
```

    
    Binomial (n=10, p=0.5): [6 4 5 5 5]


### File input/output and import/export

*Setup code*


```python
import os
import tempfile
import numpy as np

# Create sample array
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Create temp directory for demo
temp_dir = tempfile.mkdtemp()

print(f"original ndarray: {arr}")
print(f"Temporary directory created at: {temp_dir}")
```

    original ndarray: [[1 2 3]
     [4 5 6]
     [7 8 9]]
    Temporary directory created at: /tmp/tmpr0nzny9i


*Save in `.npy` format (binary)*


```python
npy_path = os.path.join(temp_dir, 'array.npy')
np.save(npy_path, arr)
print(f"Saved .npy file to {npy_path}")
```

    Saved .npy file to /tmp/tmpr0nzny9i/array.npy


*Load `.npy` file*


```python
loaded_arr = np.load(npy_path)
print("Loaded from .npy:\n", loaded_arr)
```

    Loaded from .npy:
     [[1 2 3]
     [4 5 6]
     [7 8 9]]


*Save multiple arrays as `.npz` (compressed)*


```python
npz_path = os.path.join(temp_dir, 'arrays.npz')
arr2 = np.array([10, 20, 30, 40])
np.savez(npz_path, array1=arr, array2=arr2)
print(f"\nSaved .npz file to {npz_path}")
```

    
    Saved .npz file to /tmp/tmpr0nzny9i/arrays.npz


*Load `.npz` file*


```python
loaded = np.load(npz_path)
print("Loaded from .npz:")
print("  array1:\n", loaded['array1'])
print("  array2:", loaded['array2'])
```

    Loaded from .npz:
      array1:
     [[1 2 3]
     [4 5 6]
     [7 8 9]]
      array2: [10 20 30 40]


*Save as a text file (CSV-like format)*


```python
txt_path = os.path.join(temp_dir, 'array.txt')
np.savetxt(txt_path, arr, delimiter=',', fmt='%d')
print(f"\nSaved text file to {txt_path}")
```

    
    Saved text file to /tmp/tmpr0nzny9i/array.txt


*Load from a text file*


```python
loaded_txt = np.loadtxt(txt_path, delimiter=',')
print("Loaded from text:\n", loaded_txt)
```

    Loaded from text:
     [[1. 2. 3.]
     [4. 5. 6.]
     [7. 8. 9.]]


### Useful functions and advanced techniques

*Apply a function to each element*


```python
arr = np.array([1, 2, 3, 4, 5])
squared = np.vectorize(lambda x: x**2)(arr)
print("Vectorized function (square):", squared)
```

    Vectorized function (square): [ 1  4  9 16 25]


*Piecewise operations*


```python
arr = np.array([1, 2, 3, 4, 5])
result = np.piecewise(arr, [arr < 3, arr >= 3], [lambda x: x**2, lambda x: x*10])
print("\nPiecewise (x<3: x², x≥3: 10x):", result)
```

    
    Piecewise (x<3: x², x≥3: 10x): [ 1  4 30 40 50]


*Apply operations along an axis*


```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
sums0 = np.apply_along_axis(np.sum, axis=0, arr=matrix)
sums1 = np.apply_along_axis(np.sum, axis=1, arr=matrix)

print("\nApply sum along axis 0:", sums0)
print("Apply sum along axis 1:", sums1)

```

    
    Apply sum along axis 0: [5 7 9]
    Apply sum along axis 1: [ 6 15]


*Repeat and tile*


```python
arr = np.array([1, 2, 3])
print("\nRepeat (each element 2 times):", np.repeat(arr, 2))
print("Tile (whole array 2 times):", np.tile(arr, 2))
```

    
    Repeat (each element 2 times): [1 1 2 2 3 3]
    Tile (whole array 2 times): [1 2 3 1 2 3]


*Reduction operations*


```python
arr = np.array([1, 2, 3, 4, 5])
result = np.add.reduce(arr)  # Sum
print("\nReduce with add (sum):", result)
```

    
    Reduce with add (sum): 15


*`searchsorted` (binary search)*


```python
sorted_arr = np.array([1, 3, 5, 7, 9])
indices = np.searchsorted(sorted_arr, [2, 4, 6, 8])
print("\nSearchsorted indices:", indices)
```

    
    Searchsorted indices: [1 2 3 4]


*Extract diagonal elements*


```python
matrix = np.arange(9).reshape(3, 3)
diagonal0 = np.diag(matrix, k=0)  # Main diagonal
diagonal1 = np.diag(matrix, k=1)  # Diagonal above main
print("\nDiagonal of matrix:\n", matrix)
print("Diagonal elements:", diagonal0)
print("Diagonal above main:", diagonal1)
```

    
    Diagonal of matrix:
     [[0 1 2]
     [3 4 5]
     [6 7 8]]
    Diagonal elements: [0 4 8]
    Diagonal above main: [1 5]


*Create a diagonal matrix*


```python
diag_matrix = np.diag([1, 2, 3])
print("\nDiagonal matrix from [1, 2, 3]:\n", diag_matrix)
```

    
    Diagonal matrix from [1, 2, 3]:
     [[1 0 0]
     [0 2 0]
     [0 0 3]]


*Count and display non-zero values*


```python
arr = np.array([0, 1, 0, 2, 3, 0])
print("\nNonzero count:", np.count_nonzero(arr))
print("Nonzero indices:", np.nonzero(arr))
```

    
    Nonzero count: 3
    Nonzero indices: (array([1, 3, 4]),)


### Tips, techniques, and performance

*Setup code*


```python
import time
```

*Avoid Python loops by using vectorisation*


```python
arr = np.arange(1_000_000)

# Slow: Python loop
start = time.time()
result = np.array([x**2 for x in arr])
loop_time = time.time() - start
print(f"Python loop: {loop_time:.6f} seconds")

# Fast: NumPy vectorization
start = time.time()
result = arr ** 2
vectorized_time = time.time() - start
print(f"NumPy vectorized: {vectorized_time:.6f} seconds")
print(f"Speedup: {loop_time/vectorized_time:.1f}x faster\n")
```

    === Performance: Vectorization ===
    Python loop: 0.238411 seconds
    NumPy vectorized: 0.001625 seconds
    Speedup: 146.7x faster
    


*Use in-place operations where appropriate*


```python
arr = np.arange(5)
print("Original:", arr)
arr += 10  # In-place (more memory efficient)
print("After += 10:", arr)
```

    Original: [0 1 2 3 4]
    After += 10: [10 11 12 13 14]


*Data types and memory usage*


```python
arr_float64 = np.arange(1000, dtype=np.float64)
arr_float32 = np.arange(1000, dtype=np.float32)
arr_int32 = np.arange(1000, dtype=np.int32)

print(f"Float64: {arr_float64.nbytes} bytes")
print(f"Float32: {arr_float32.nbytes} bytes")
print(f"Int32: {arr_int32.nbytes} bytes")
```

    Float64: 8000 bytes
    Float32: 4000 bytes
    Int32: 4000 bytes


*Memory efficiency: views versus copies*


```python
original = np.arange(10)
view = original[:]  # This is a view, shares memory
copy = original[:].copy()  # This is a copy

print(f"View shares memory: {view.base is original}")
print(f"Copy doesn't share memory: {copy.base is original}")
```

    View shares memory: True
    Copy doesn't share memory: False


*Useful diagnostics for debugging*


```python
arr = np.random.randn(3, 4, 5)

print(f"Shape: {arr.shape}")
print(f"Ndim: {arr.ndim}")
print(f"Dtype: {arr.dtype}")
print(f"Size: {arr.size}")
print(f"Memory: {arr.nbytes} bytes")
```

    Shape: (3, 4, 5)
    Ndim: 3
    Dtype: float64
    Size: 60
    Memory: 480 bytes


*Check for NaN and infinite values*


```python
arr = np.array([1, 2, np.nan, 4, np.inf, -np.inf])

print(f"Array: {arr}")
print(f"Has NaN: {np.isnan(arr).any()}")
print(f"Has Inf: {np.isinf(arr).any()}")
print(f"Is finite: {np.isfinite(arr)}")
```

    Array: [  1.   2.  nan   4.  inf -inf]
    Has NaN: True
    Has Inf: True
    Is finite: [ True  True False  True False False]


*Type casting*


```python
arr = np.array([1.5, 2.7, 3.2])

print(f"Original (float): {arr}")
print(f"As int: {arr.astype(int)}")
print(f"As str: {arr.astype(str)}")
```

    Original (float): [1.5 2.7 3.2]
    As int: [1 2 3]
    As str: ['1.5' '2.7' '3.2']


## Conclusion

NumPy is a core component of scientific computing in Python. This tutorial has outlined how NumPy arrays differ from Python lists, how they can be created and inspected, and how indexing, arithmetic, and statistical operations can be performed efficiently.

A key strength of NumPy lies in its speed and vectorised programming model. Rather than relying on explicit Python loops for every calculation, practitioners can apply concise operations to complete datasets. This capability makes NumPy an essential tool for data analysis, machine learning, and numerical modelling.

To develop proficiency, practise regularly with arrays of different shapes, slicing patterns, and reshaping strategies. Comparing NumPy workflows with equivalent pure-Python approaches is particularly useful for understanding performance and expressiveness benefits. These foundations also support more advanced work with libraries such as Pandas, SciPy, and TensorFlow.

This article has presented a concise, practice-oriented reference for fundamental NumPy workflows. For continued development, readers are encouraged to extend these examples to domain-specific datasets and to evaluate computational trade-offs in realistic analytical pipelines.

Did this article help you? Let me know in the comments below, and don't forget to drop a like if you enjoyed the read! Thank you.
