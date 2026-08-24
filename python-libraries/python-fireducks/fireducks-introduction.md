# Speed Up Data Processing using Fireducks
Everyone wants to create application fast as flash. There are plenty of technics which can help with this goal. In our today's article we are going to have a Python library FireDucks. FireDucks is a compiler-accelerated DataFrame library which can almost replace Pandas, using exactly same syntax as Pandas, but it is multithreaded. It is designed to speed up our data projects by up 20x-100x times without requirement to rewrite single Pandas code. It is using JIT (Just-In-Time) compilation, multithreading, and lazy executin model just like Polars or Apache Spark.

## Core Performance Differences
As it was written earlies, syntax is same with Pandas, but they both work differently in the background.
- **Lazy vs. Eager Execution:** Pandas evaluates every line of code instantly, eager processing, but FireDucks creates an internal graph and delays execution until we trigger an action like `.show()`, print(), or exporting to a `.csv` format. This is called lazy processing.
- **Automatic Fallback:** There are still methods in FireDucks which are not implemented yet. It will automatically convert data into standard Pandas, process it, and convert them back to FireDucks format.

We can get information about automatic fallbacks by enabling logs in terminal by using environment variable -Wfallback. We can either set it to our system, or use [dotenv](https://medium.com/@michal.puzanov/python-dotenv-library-introduction-dfb492c5304b), to add it temporary, when our application runs.
```
export FIREDUCKS_FLAGS="-Wfallback"
```
## Python Installation Requirements
FireDucks supports the releases Python 3.9 up to Python 3.13 (without free-threaded).
### Crucial Compatibility Limits
- **Python 3.14 and Newer:** FireDucks explicitly caps its requirements at `< 3.14`. Trying to install it on Python 3.14 versions will trigger a `No matching distribution found` error.
- **Python 3.8 and Older:** Since version 1.1.0, FireDucks upraded its internal dependencies (pyarrow), and completely drop support for Python <= 3.8.
- **Platform Restiction:** Pthon version aside, ensure we are running Linux (x86_64) or macOS (Apple Silicon / ARM). Native Windows is not yet supported, but Windows developers can use Python inside WSL (Windows Subsystem for Linux).



