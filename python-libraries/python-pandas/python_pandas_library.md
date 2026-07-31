# Python Pandas Library

Pandas is an open-source library for data analysis and manipulation in Python. It provides fast, flexible and expressive data structures for working with relational and labelled data. Originally developed by Wes McKinney in 2008, it has become a foundational tool in modern data science and serves as a highly programmable analogue to spreadsheet software.

## Key characteristics
- **NumPy foundation:** Built on top of NumPy, it inherits highly optimised, array-based computational performance.
- **Label-driven alignment:** Data are automatically aligned according to explicit row and column labels, thereby improving the reliability of calculations involving partially mismatched datasets.
- **Heterogeneous typing:** Unlike strict numerical arrays, Pandas can accommodate mixed data types, including integers, strings, floats and booleans, within a single tabular structure.
- **Missing-data resilience:** It provides native support for detecting, representing and handling missing values, such as NaN.

## Core data structures
- **Series:** A one-dimensional labelled array capable of holding any data type. In practical terms, it resembles a single column in a spreadsheet.
- **DataFrame:** A two-dimensional tabular data structure with labelled rows and columns. It may be regarded as a collection of Series sharing a common index, analogous to a table in SQL or a worksheet in Excel.

## Core features and capabilities
- **Robust input/output parsing:** Pandas supports efficient reading and writing across multiple formats, including CSV, Excel, SQL databases, JSON and Parquet.
- **Advanced data cleaning:** Built-in methods enable users to identify, filter and remove duplicates, and to impute missing values.
- **Flexible wrangling and reshaping:** The library facilitates pivoting, melting, slicing and subsetting operations based on conditional logic.
- **High-performance merging:** Relational operations such as inner, outer, left and right joins, as well as concatenation, can be executed in concise code.
- **Split-apply-combine (GroupBy):** Data may be grouped by specified criteria and summarised using aggregate operations such as sums, averages and custom calculations.
- **Time-series functionality:** Pandas provides specialised tools for handling dates, converting time zones, generating date ranges and resampling time-stamped data.
- **Integrated plotting:** It offers Matplotlib-based plotting utilities, enabling the rapid visualisation of tabular data with the .plot() interface.

Time-series functionality and integrated plotting are not covered in this article.

## Practical examples

### Installation

Using pip:
<pre>pip install pandas</pre>

Using conda:
<pre>conda install pandas</pre>

Using poetry:
<pre>poetry add pandas</pre>

### Verify the installation
The following script may be used to confirm that pandas has been installed correctly.


```python
import pandas as pd

print(pd.__version__)
```

    3.0.5


### Creating DataFrame
*from dictionary*



```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['NYC', 'LA', 'Chicago']
})

print(df)
```

          name  age     city
    0    Alice   25      NYC
    1      Bob   30       LA
    2  Charlie   35  Chicago


*from dictionary using NumPy*


```python
import numpy as np

df_dict = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': np.linspace(25, 35, num=3, dtype=int),
    'city': ['NYC', 'LA', 'Chicago']
})

print(df_dict)
```

          name  age     city
    0    Alice   25      NYC
    1      Bob   30       LA
    2  Charlie   35  Chicago


*from list of lists*


```python
df_list = pd.DataFrame(
    [['Alice', 25, 'NYC' ], ['Bob', 30, 'LA'], ['Charlie', 35, 'Chicago']], 
    columns=['name', 'age', 'city']
)

print(df_list)
```

          name  age     city
    0    Alice   25      NYC
    1      Bob   30       LA
    2  Charlie   35  Chicago


*from ndarray*


```python
df_ndarray = pd.DataFrame(
    np.array([['Alice', 25, 'NYC'], ['Bob', 30, 'LA'], ['Charlie', 35, 'Chicago']]),
    columns=['name', 'age', 'city']
)

print(df_ndarray)
```

          name age     city
    0    Alice  25      NYC
    1      Bob  30       LA
    2  Charlie  35  Chicago


### Data inspection and information

*basic info*


```python
print(f"Shape: {df.shape}")  # (rows, columns)
print(f"Column names: {df.columns.tolist()}")
print(f"Data types:\n{df.dtypes}\n")
print(f"DataFrame Info:\n{df.info()}\n")
```

    Shape: (3, 3)
    Column names: ['name', 'age', 'city']
    Data types:
    name      str
    age     int64
    city      str
    dtype: object
    
    <class 'pandas.DataFrame'>
    RangeIndex: 3 entries, 0 to 2
    Data columns (total 3 columns):
     #   Column  Non-Null Count  Dtype
    ---  ------  --------------  -----
     0   name    3 non-null      str  
     1   age     3 non-null      int64
     2   city    3 non-null      str  
    dtypes: int64(1), str(2)
    memory usage: 204.0 bytes
    DataFrame Info:
    None
    


*head and tail*


```python
print(f"First default number of rows:\n{df.head()}\n")
print(f"First 2 rows:\n{df.head(2)}\n")
print(f"Last default number of rows:\n{df.tail()}\n")
print(f"Last 2 rows:\n{df.tail(2)}")
```

    First default number of rows:
          name  age     city
    0    Alice   25      NYC
    1      Bob   30       LA
    2  Charlie   35  Chicago
    
    First 2 rows:
        name  age city
    0  Alice   25  NYC
    1    Bob   30   LA
    
    Last default number of rows:
          name  age     city
    0    Alice   25      NYC
    1      Bob   30       LA
    2  Charlie   35  Chicago
    
    Last 2 rows:
          name  age     city
    1      Bob   30       LA
    2  Charlie   35  Chicago


*descriptive statistics for numerical columns*


```python
print(df.describe())
```

            age
    count   3.0
    mean   30.0
    std     5.0
    min    25.0
    25%    27.5
    50%    30.0
    75%    32.5
    max    35.0


*descriptive statistics for all columns with transpose layout*


```python
print(df.describe(include='all').T)
```

         count unique    top freq  mean  std   min   25%   50%   75%   max
    name     3      3  Alice    1   NaN  NaN   NaN   NaN   NaN   NaN   NaN
    age    3.0    NaN    NaN  NaN  30.0  5.0  25.0  27.5  30.0  32.5  35.0
    city     3      3    NYC    1   NaN  NaN   NaN   NaN   NaN   NaN   NaN


*unique and missing values*


```python
print(f"Unique values in 'name':\n {df['name'].unique()}\n")
print(f"Null values:\n {df.isnull().sum()}\n")
```

    Unique values in 'name':
     <StringArray>
    ['Alice', 'Bob', 'Charlie']
    Length: 3, dtype: str
    
    Null values:
     name    0
    age     0
    city    0
    dtype: int64
    


### Selecting data by columns and rows
*select column - returns Series*


```python
print(df['name'])
```

    0      Alice
    1        Bob
    2    Charlie
    Name: name, dtype: str


*select multiple columns*


```python
print(df[['name', 'age']])
```

          name  age
    0    Alice   25
    1      Bob   30
    2  Charlie   35


*select by position (iloc)*


```python
print("Select first 2 rows, first 2 columns (iloc):")
print(df.iloc[0:2, 0:2])
```

    Select first 2 rows, first 2 columns (iloc):
        name  age
    0  Alice   25
    1    Bob   30


*select by label (loc)*


```python
print("Select by label using loc:")
print(df.loc[0])  # First row
print(df.loc[0:1, ['name', 'age']])  # First 2 rows, specific columns
```

    Select by label using loc:
    name    Alice
    age        25
    city      NYC
    Name: 0, dtype: object
        name  age
    0  Alice   25
    1    Bob   30


### Filtering and conditional selection
*simple filter*


```python
print(df[df['age'] > 25])
```

          name  age     city
    1      Bob   30       LA
    2  Charlie   35  Chicago


*multiple conditions with AND*


```python
print("Age > 25 AND city == 'LA':")
print(df[(df['age'] > 25) & (df['city'] == 'LA')])
```

    Age > 25 AND city == 'LA':
      name  age city
    1  Bob   30   LA


*multiple conditions with OR*


```python
print("Age == 25 OR city == 'Chicago':")
print(df[(df['age'] == 25) | (df['city'] == 'Chicago')])
```

    Age == 25 OR city == 'Chicago':
          name  age     city
    0    Alice   25      NYC
    2  Charlie   35  Chicago


*multiple values using list*


```python
print("City in ['NYC', 'Chicago']:")
print(df[df['city'].isin(['NYC', 'Chicago'])])
```

    City in ['NYC', 'Chicago']:
          name  age     city
    0    Alice   25      NYC
    2  Charlie   35  Chicago


*string filtering*


```python
print("City starts with 'L':")
print(df[df['city'].str.startswith('L')])
```

    City starts with 'L':
      name  age city
    1  Bob   30   LA


*filter using query method*


```python
print(df.query('age > 25'))
```

          name  age     city
    1      Bob   30       LA
    2  Charlie   35  Chicago


### Adding and modifying columns

It is good practice to avoid modifying the original DataFrame when adding, deleting or altering data. For this reason, a deep copy of the DataFrame is used in the examples that follow.

*hard copy dataframe*


```python
df_copy = df.copy()

print(f"Copy of Original DataFrame: \n{df_copy}\n")
```

    Copy of Original DataFrame: 
          name  age     city
    0    Alice   25      NYC
    1      Bob   30       LA
    2  Charlie   35  Chicago
    


*add new column*


```python
df_copy['age_next_year'] = df_copy['age'] + 1

print(df_copy)
```

          name  age     city  age_next_year
    0    Alice   25      NYC             26
    1      Bob   30       LA             31
    2  Charlie   35  Chicago             36


*modify existing column with lambda function*


```python
df_copy['age_group'] = df_copy['age'].apply(lambda x: 'Young' if x < 30 else 'Older')

print(df_copy)
```

          name  age     city  age_next_year age_group
    0    Alice   25      NYC             26     Young
    1      Bob   30       LA             31     Older
    2  Charlie   35  Chicago             36     Older


*conditional assignment (using np.where)*


```python
df_copy['status'] = np.where(df_copy['age'] > 25, 'Senior', 'Junior')

print(df_copy)
```

          name  age     city  age_next_year age_group  status
    0    Alice   25      NYC             26     Young  Junior
    1      Bob   30       LA             31     Older  Senior
    2  Charlie   35  Chicago             36     Older  Senior


*rename columns*


```python
df_copy = df_copy.rename(columns={'name': 'full_name', 'city': 'location'})
print(df_copy)

df_copy.rename(columns={'full_name': 'name', 'location': 'city'}, inplace=True)
print(df_copy)

```

    Rename columns:
      full_name  age location  age_next_year age_group  status
    0     Alice   25      NYC             26     Young  Junior
    1       Bob   30       LA             31     Older  Senior
    2   Charlie   35  Chicago             36     Older  Senior
    Rename columns back using inplace:
          name  age     city  age_next_year age_group  status
    0    Alice   25      NYC             26     Young  Junior
    1      Bob   30       LA             31     Older  Senior
    2  Charlie   35  Chicago             36     Older  Senior


*drop columns*


```python
df_dropped = df_copy.drop(columns=['city'])

print(df_dropped)
```

          name  age  age_next_year age_group  status
    0    Alice   25             26     Young  Junior
    1      Bob   30             31     Older  Senior
    2  Charlie   35             36     Older  Senior


### Data cleaning and missing values
*sample dataframe with missing values*


```python
df_missing = pd.DataFrame({
    'name': ['Alice', None, 'Charlie', None],
    'age': [25, 30, np.nan, 40],
    'city': ['NYC', None, 'Chicago', 'LA']
})

print("DataFrame with missing values:")
print(df_missing)
```

    DataFrame with missing values:
          name   age     city
    0    Alice  25.0      NYC
    1      NaN  30.0      NaN
    2  Charlie   NaN  Chicago
    3      NaN  40.0       LA


*check for missing values using info*


```python
print(df_missing.info())
```

    <class 'pandas.DataFrame'>
    RangeIndex: 4 entries, 0 to 3
    Data columns (total 3 columns):
     #   Column  Non-Null Count  Dtype  
    ---  ------  --------------  -----  
     0   name    2 non-null      str    
     1   age     3 non-null      float64
     2   city    3 non-null      str    
    dtypes: float64(1), str(2)
    memory usage: 228.0 bytes
    None


There are four records in the sample DataFrame. The 'name' column contains two non-null values, while the 'age' and 'city' columns contain three non-null values each.


```python
print(f"Check for missing values:\n{df_missing.isnull()}\n")
print(f"Check for missing values:\n{df_missing.isnull().sum()}\n")
```

    Check for missing values:
        name    age   city
    0  False  False  False
    1   True  False   True
    2  False   True  False
    3   True  False  False
    
    Check for missing values:
    name    2
    age     1
    city    1
    dtype: int64
    


*drop rows with missing values*


```python
# Drop rows with any missing values
print(f"{df_missing.dropna()}\n")

# Drop rows where specific column is missing
print(df_missing.dropna(subset=['age']))
```

    Drop rows with missing values:
        name   age city
    0  Alice  25.0  NYC
    
    Drop rows where 'age' is missing:
        name   age city
    0  Alice  25.0  NYC
    1    NaN  30.0  NaN
    3    NaN  40.0   LA


*fill missing values*


```python
# Fill missing values with 0
print(df_missing.fillna(0))
print()

# Fill missing values with forward fill
print(df_missing.ffill())
print()

# Fill with mean
df_missing['age'] = df_missing['age'].fillna(df_missing['age'].mean())
print(df_missing)
print()

```

          name   age     city
    0    Alice  25.0      NYC
    1        0  30.0        0
    2  Charlie   0.0  Chicago
    3        0  40.0       LA
    
          name   age     city
    0    Alice  25.0      NYC
    1    Alice  30.0      NYC
    2  Charlie  30.0  Chicago
    3  Charlie  40.0       LA
    
          name        age     city
    0    Alice  25.000000      NYC
    1      NaN  30.000000      NaN
    2  Charlie  31.666667  Chicago
    3      NaN  40.000000       LA
    


### Grouping and aggregation

*sample dataframe*


```python
df_sales = pd.DataFrame({
    'department': ['Sales', 'Sales', 'IT', 'IT', 'HR', 'HR'],
    'employee': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
    'salary': [50000, 55000, 75000, 75000, 45000, 48000],
    'bonus': [5000, 6000, 10000, 12000, 3000, 2000]
})
print(df_sales)
```

      department employee  salary  bonus
    0      Sales    Alice   50000   5000
    1      Sales      Bob   55000   6000
    2         IT  Charlie   75000  10000
    3         IT    David   75000  12000
    4         HR      Eve   45000   3000
    5         HR    Frank   48000   2000


*group by single column*


```python
print(df_sales.groupby('department')['salary'].mean())
```

    department
    HR       46500.0
    IT       75000.0
    Sales    52500.0
    Name: salary, dtype: float64


*group by and aggregate multiple columns*


```python
agg_result = df_sales.groupby('department').agg({
    'salary': ['mean', 'sum', 'count'],
    'bonus': 'mean'
})
print(agg_result)
```

                 salary                  bonus
                   mean     sum count     mean
    department                                
    HR          46500.0   93000     2   2500.0
    IT          75000.0  150000     2  11000.0
    Sales       52500.0  105000     2   5500.0


*custom aggregation names*


```python
print(df_sales.groupby('department').agg(
    avg_salary=('salary', 'mean'),
    total_bonus=('bonus', 'sum'),
    count=('employee', 'count')
))
```

                avg_salary  total_bonus  count
    department                                
    HR             46500.0         5000      2
    IT             75000.0        22000      2
    Sales          52500.0        11000      2


*group by multiple columns*


```python
df_sales['year'] = [2023, 2023, 2024, 2024, 2023, 2024]

print(df_sales.groupby(['department', 'year'])['salary'].mean())
```

    department  year
    HR          2023    45000.0
                2024    48000.0
    IT          2024    75000.0
    Sales       2023    52500.0
    Name: salary, dtype: float64


### Sorting and ranking

*sort by single column ascending*


```python
print(df_sales.sort_values('salary'))
```

      department employee  salary  bonus  year
    4         HR      Eve   45000   3000  2023
    5         HR    Frank   48000   2000  2024
    0      Sales    Alice   50000   5000  2023
    1      Sales      Bob   55000   6000  2023
    3         IT    David   75000  12000  2024
    2         IT  Charlie   75000  10000  2024


*sort by single column descending*


```python
print(df_sales.sort_values('salary', ascending=False))
```

      department employee  salary  bonus  year
    3         IT    David   75000  12000  2024
    2         IT  Charlie   75000  10000  2024
    1      Sales      Bob   55000   6000  2023
    0      Sales    Alice   50000   5000  2023
    5         HR    Frank   48000   2000  2024
    4         HR      Eve   45000   3000  2023


*sort by multiple columns*


```python
print(df_sales.sort_values(['department', 'salary']))
```

      department employee  salary  bonus  year
    4         HR      Eve   45000   3000  2023
    5         HR    Frank   48000   2000  2024
    2         IT  Charlie   75000  10000  2024
    3         IT    David   75000  12000  2024
    0      Sales    Alice   50000   5000  2023
    1      Sales      Bob   55000   6000  2023


*sort by index*


```python
# create a new DataFrame with 'employee' as the index
df_index = df_sales.set_index('employee')

print(df_index.sort_index())
```

             department  salary  bonus  year
    employee                                
    Alice         Sales   50000   5000  2023
    Bob           Sales   55000   6000  2023
    Charlie          IT   75000  10000  2024
    David            IT   75000  12000  2024
    Eve              HR   45000   3000  2023
    Frank            HR   48000   2000  2024


*ranking*


```python
df_sales['salary_rank'] = df_sales['salary'].rank(ascending=False)

print(df_sales[['employee', 'salary', 'salary_rank']])
```

      employee  salary  salary_rank
    0    Alice   50000          4.0
    1      Bob   55000          3.0
    2  Charlie   75000          1.5
    3    David   75000          1.5
    4      Eve   45000          6.0
    5    Frank   48000          5.0


*dense ranking*


```python
df_sales['salary_dense_rank'] = df_sales['salary'].rank(method='dense', ascending=False)

print(df_sales[['employee', 'salary', 'salary_dense_rank']])
```

      employee  salary  salary_dense_rank
    0    Alice   50000                3.0
    1      Bob   55000                2.0
    2  Charlie   75000                1.0
    3    David   75000                1.0
    4      Eve   45000                5.0
    5    Frank   48000                4.0


### Merging and joining DataFrames

*sample dataframes df1, df2 and df3*


```python
df1 = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'department': ['Sales', 'IT', 'HR']
})

df2 = pd.DataFrame({
    'id': [1, 2, 3],
    'salary': [50000, 70000, 45000],
    'bonus': [5000, 10000, 3000]
})

print(df1)
print()
print(df2)
```

       id     name department
    0   1    Alice      Sales
    1   2      Bob         IT
    2   3  Charlie         HR
    
       id  salary  bonus
    0   1   50000   5000
    1   2   70000  10000
    2   3   45000   3000


*inner join (intersection)*


```python
print(pd.merge(df1, df2, on='id'))
```

       id     name department  salary  bonus
    0   1    Alice      Sales   50000   5000
    1   2      Bob         IT   70000  10000
    2   3  Charlie         HR   45000   3000


*left join*


```python
df3 = pd.DataFrame({
    'id': [1, 2, 4],
    'salary': [50000, 70000, 80000]
})

print(pd.merge(df1, df3, on='id', how='left'))
```

       id     name department   salary
    0   1    Alice      Sales  50000.0
    1   2      Bob         IT  70000.0
    2   3  Charlie         HR      NaN


*right join*


```python
print(pd.merge(df1, df3, on='id', how='right'))
```

       id   name department  salary
    0   1  Alice      Sales   50000
    1   2    Bob         IT   70000
    2   4    NaN        NaN   80000


*outer join (union)*


```python
print(pd.merge(df1, df3, on='id', how='outer'))
```

       id     name department   salary
    0   1    Alice      Sales  50000.0
    1   2      Bob         IT  70000.0
    2   3  Charlie         HR      NaN
    3   4      NaN        NaN  80000.0


*concatenate vertically*


```python
print(pd.concat([df1, df1], ignore_index=True))
```

       id     name department
    0   1    Alice      Sales
    1   2      Bob         IT
    2   3  Charlie         HR
    3   1    Alice      Sales
    4   2      Bob         IT
    5   3  Charlie         HR


*concatenate horizontally*


```python
print(pd.concat([df1, df2], axis=1))
```

       id     name department  id  salary  bonus
    0   1    Alice      Sales   1   50000   5000
    1   2      Bob         IT   2   70000  10000
    2   3  Charlie         HR   3   45000   3000


### Reshaping data using pivot tables

*sample dataframe1*


```python
df_pivot = pd.DataFrame({
    'product': ['A', 'A', 'B', 'B', 'C', 'C'],
    'month': ['Jan', 'Feb', 'Jan', 'Feb', 'Jan', 'Feb'],
    'sales': [100, 150, 200, 250, 300, 350]
})

print(df_pivot)
```

      product month  sales
    0       A   Jan    100
    1       A   Feb    150
    2       B   Jan    200
    3       B   Feb    250
    4       C   Jan    300
    5       C   Feb    350


*pivot table*


```python
pivot = df_pivot.pivot(index='product', columns='month', values='sales')

print(pivot)
```

    month    Feb  Jan
    product          
    A        150  100
    B        250  200
    C        350  300


*sample dataframe2*


```python
df_pivot2 = pd.DataFrame({
    'category': ['A', 'A', 'A', 'B', 'B', 'B'],
    'region': ['North', 'South', 'North', 'South', 'North', 'South'],
    'sales': [100, 150, 120, 200, 250, 300]
})

print(df_pivot2)
```

      category region  sales
    0        A  North    100
    1        A  South    150
    2        A  North    120
    3        B  South    200
    4        B  North    250
    5        B  South    300


*pivot with aggregation*


```python
pivot_agg = df_pivot2.pivot_table(
    index='category', 
    columns='region', 
    values='sales', 
    aggfunc='sum'
)

print(pivot_agg)
```

    region    North  South
    category              
    A           220    150
    B           250    500


*unstack*


```python
df_stacked = df_pivot.set_index(['product', 'month'])['sales']
df_unstacked = df_stacked.unstack()

print(df_stacked)
print()
print(df_unstacked)
```

    product  month
    A        Jan      100
             Feb      150
    B        Jan      200
             Feb      250
    C        Jan      300
             Feb      350
    Name: sales, dtype: int64
    
    month    Feb  Jan
    product          
    A        150  100
    B        250  200
    C        350  300


*melt (unpivot)*


```python
df_melted = pd.melt(df_unstacked.reset_index(), id_vars=['product'], var_name='variable', value_name='value')

print(df_melted)
```

      product variable  value
    0       A      Feb    150
    1       B      Feb    250
    2       C      Feb    350
    3       A      Jan    100
    4       B      Jan    200
    5       C      Jan    300


### String operations

*sample dataframe*


```python
df_str = pd.DataFrame({
    'name': ['alice smith', 'bob jones', 'charlie brown'],
    'email': ['alice@email.com', 'bob@email.com', 'charlie@email.com']
})

print(df_str)
```

                name              email
    0    alice smith    alice@email.com
    1      bob jones      bob@email.com
    2  charlie brown  charlie@email.com


*string upper, title case*


```python
print(df_str['name'].str.upper())
print()

print(df_str['name'].str.title())
print()
```

    0      ALICE SMITH
    1        BOB JONES
    2    CHARLIE BROWN
    Name: name, dtype: str
    
    0      Alice Smith
    1        Bob Jones
    2    Charlie Brown
    Name: name, dtype: str
    


*string lenght*


```python
print(df_str['name'].str.len())
```

    0    11
    1     9
    2    13
    Name: name, dtype: int64


*string contains*


```python
print(df_str[df_str['name'].str.contains('alice')])
```

              name            email
    0  alice smith  alice@email.com


*extract part of string*


```python
print(df_str['name'].str.split(' ').str[0])
print()
print(df_str['name'].str.split(' ').str[1])
```

    0      alice
    1        bob
    2    charlie
    Name: name, dtype: object
    
    0    smith
    1    jones
    2    brown
    Name: name, dtype: object


*replace part of string*


```python
print(df_str['name'].str.replace('smith', 'Smith'))
```

    0      alice Smith
    1        bob jones
    2    charlie brown
    Name: name, dtype: str


*extract digits from string*


```python
df_codes = pd.DataFrame({'code': ['A123', 'B456', 'C789']})
print(df_codes)
print()

df_codes['code'] = df_codes['code'].str.replace(r'\D', '', regex=True)
print(df_codes)

```

       code
    0  A123
    1  B456
    2  C789
    
      code
    0  123
    1  456
    2  789


*get domain from email address*


```python
print(df_str['email'].str.extract(r'@([a-z]+)\.com'))
```

           0
    0  email
    1  email
    2  email


### Datetime operations

*sample dataframe*


```python
df_dates = pd.DataFrame({
    'date': ['2024-01-15', '2024-02-20', '2024-03-10'],
    'value': [100, 150, 200]
})

print(df_dates)
print(df_dates.dtypes)
```

             date  value
    0  2024-01-15    100
    1  2024-02-20    150
    2  2024-03-10    200
    date       str
    value    int64
    dtype: object


*convert to datetime type*


```python
df_dates['date'] = pd.to_datetime(df_dates['date'])

print(df_dates)
print(df_dates.dtypes)
```

            date  value
    0 2024-01-15    100
    1 2024-02-20    150
    2 2024-03-10    200
    date     datetime64[us]
    value             int64
    dtype: object


*extract components*


```python
df_dates['year'] = df_dates['date'].dt.year
df_dates['month'] = df_dates['date'].dt.month
df_dates['day'] = df_dates['date'].dt.day
df_dates['day_name'] = df_dates['date'].dt.day_name()

print(df_dates)
```

            date  value  year  month  day day_name
    0 2024-01-15    100  2024      1   15   Monday
    1 2024-02-20    150  2024      2   20  Tuesday
    2 2024-03-10    200  2024      3   10   Sunday


*date add 10 days*


```python
print(df_dates['date'] + pd.Timedelta(days=10))
```

    0   2024-01-25
    1   2024-03-01
    2   2024-03-20
    Name: date, dtype: datetime64[us]


*date range 5 days*


```python
date_range = pd.date_range(start='2024-01-01', periods=5, freq='D')

print(date_range)
```

    DatetimeIndex(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04',
                   '2024-01-05'],
                  dtype='datetime64[us]', freq='D')


*filter by date*


```python
start_date = pd.to_datetime('2024-02-01')
end_date = pd.to_datetime('2024-03-01')
df_filtered = df_dates[(df_dates['date'] >= start_date) & (df_dates['date'] <= end_date)]

print(df_filtered)
```

            date  value  year  month  day day_name
    1 2024-02-20    150  2024      2   20  Tuesday


### Mathematical and statistical operations

*sample dataframe*


```python
df_math = pd.DataFrame({
    'A': [10, 20, 30, 40, 50],
    'B': [5, 10, 15, 20, 25],
    'C': [1, 2, 3, 4, 5]
})

print(df_math)
```

        A   B  C
    0  10   5  1
    1  20  10  2
    2  30  15  3
    3  40  20  4
    4  50  25  5


*basic statistics*


```python
print(f"Mean: {df_math['A'].mean()}")
print(f"Median: {df_math['A'].median()}")
print(f"Std Dev: {df_math['A'].std()}")
print(f"Min: {df_math['A'].min()}")
print(f"Max: {df_math['A'].max()}")
print(f"Sum: {df_math['A'].sum()}")
```

    Mean: 30.0
    Median: 30.0
    Std Dev: 15.811388300841896
    Min: 10
    Max: 50
    Sum: 150


*percentiles*


```python
print(f"25th percentile: {df_math['A'].quantile(0.25)}")
print(f"75th percentile: {df_math['A'].quantile(0.75)}")
```

    25th percentile: 20.0
    75th percentile: 40.0


*correlation*


```python
print(df_math.corr())
```

         A    B    C
    A  1.0  1.0  1.0
    B  1.0  1.0  1.0
    C  1.0  1.0  1.0


*covariance*


```python
print(df_math.cov())
```

           A      B     C
    A  250.0  125.0  25.0
    B  125.0   62.5  12.5
    C   25.0   12.5   2.5


*arithmetic operations*


```python
df_math['A_add_B'] = df_math['A'] + df_math['B']
df_math['A_subtract_B'] = df_math['A'] - df_math['B']
df_math['A_squared'] = df_math['A'] ** 2

print(df_math)
```

        A   B  C  A_add_B  A_subtract_B  A_squared
    0  10   5  1       15             5        100
    1  20  10  2       30            10        400
    2  30  15  3       45            15        900
    3  40  20  4       60            20       1600
    4  50  25  5       75            25       2500


*apply numpy function*


```python
print(df_math['A'].apply(np.sqrt))
```

    0    3.162278
    1    4.472136
    2    5.477226
    3    6.324555
    4    7.071068
    Name: A, dtype: float64


*cumulative operations*


```python
print(f"Cumulative sum of A:\n{df_math['A'].cumsum()}\n")
print(f"Cumulative product of A:\n{df_math['A'].cumprod()}\n")
```

    Cumulative sum of A:
    0     10
    1     30
    2     60
    3    100
    4    150
    Name: A, dtype: int64
    
    Cumulative product of A:
    0          10
    1         200
    2        6000
    3      240000
    4    12000000
    Name: A, dtype: int64
    


### Useful tips and best practices

*Create a copy to avoid accidental overwriting*


```python
df_copy = df.copy()
```

*use inplace carefully*


```python
df_inplace = pd.DataFrame({'A': [1, 2, 3]})
df_inplace.sort_values('A', inplace=True)
```

*Vectorised operations are generally faster than apply/loops*


```python
import time
df_large = pd.DataFrame({'A': range(10000)})

# Slow: using apply
start = time.time()
result_slow = df_large['A'].apply(lambda x: x * 2)
time_slow = time.time() - start

# Fast: vectorized
start = time.time()
result_fast = df_large['A'] * 2
time_fast = time.time() - start

print(f"  Apply time: {time_slow:.6f}s")
print(f"  Vectorized time: {time_fast:.6f}s")
```

    ✓ Vectorized operations are faster
      Apply time: 0.010587s
      Vectorized time: 0.000676s


*use groupby instead of loops*


```python
df_grouped = pd.DataFrame({
    'group': ['A', 'A', 'B', 'B'],
    'value': [1, 2, 3, 4]
})
result = df_grouped.groupby('group')['value'].sum()

print(result)
```

    ✓ Use groupby for group operations (not loops)
    group
    A    3
    B    7
    Name: value, dtype: int64


*For memory efficiency, categorical values may be preferable for repeated string data*


```python
df_mem = pd.DataFrame({'category': ['A', 'B', 'A', 'B'] * 1000})

print(f"✓ Use categorical for repeated string values")
print(f"  Object dtype: {df_mem['category'].memory_usage(deep=True)} bytes")

df_mem['category'] = df_mem['category'].astype('category')
print(f"  Categorical: {df_mem['category'].memory_usage(deep=True)} bytes")
```

    ✓ Use categorical for repeated string values
      Object dtype: 200132 bytes
      Categorical: 4232 bytes


*chaining operations*


```python
result = (df
  .query('age > 25')
  .copy()
  .assign(age_group='Senior')
  .sort_values('age', ascending=False)
)

print(result)
```

          name  age     city age_group
    2  Charlie   35  Chicago    Senior
    1      Bob   30       LA    Senior


## Conclusion

Pandas is one of the most practical and widely used libraries for data analysis in Python. This tutorial has introduced the core ideas behind creating and inspecting DataFrames, selecting and filtering data, cleaning missing values, grouping observations, and combining datasets from different sources.

A major strength of Pandas lies in its ability to make data manipulation both readable and efficient. With a small set of intuitive methods, it becomes straightforward to transform raw data into a structure suitable for exploration, reporting, or further analysis. These capabilities are especially valuable in real-world workflows where datasets are often messy, incomplete, or spread across multiple files.

To build confidence with Pandas, regular practice is essential. Readers are encouraged to experiment with the methods shown here on their own datasets, compare different approaches for the same task, and gradually explore more advanced features such as time-series handling, custom aggregations, and multi-index operations. In this way, the foundations introduced in this article can grow into a deeper and more flexible understanding of data analysis in Python.

Did this article help you? Let me know in the comments below, and don’t forget to drop a like if you enjoyed the read! Thank you.

