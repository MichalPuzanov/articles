# Asyncio Using Synchronous Python Code

## Introduction
This article examines the use of the Python `asyncio` library alongside traditional synchronous code in different environments. The `asyncio` library is particularly well suited to applications that interact with Python libraries supporting asynchronous programming. It provides the greatest benefit whenever an application encounters a bottleneck caused by network latency, third-party server responses, or heavy database communication. `asyncio` allows a single thread to handle thousands of active operations concurrently. Representative use cases include:
- **High-performance web scrapers and crawlers:** `asyncio` enables hundreds of web requests to be dispatched simultaneously using async-compatible libraries such as `httpx` or `aiohttp`. The event loop monitors all pending requests and processes each response the moment its data arrives.
- **Real-time chat applications and WebSocket servers:** Rather than creating 5,000 heavyweight operating-system threads, `asyncio` maintains all 5,000 connections within a single thread, consuming negligible CPU time whilst waiting for incoming messages.
- **Discord bots, Telegram bots, and Slack integrations:** Popular framework libraries are built directly on top of `asyncio`, allowing a single bot instance to listen for events across thousands of servers simultaneously without dropping any incoming commands.
- **Microservices and API aggregators such as FastAPI:** Using constructs such as `asyncio.TaskGroup` inside a FastAPI gateway, it is possible to query a database and multiple external APIs concurrently. The total response time is thereby reduced from the sum of all individual delays to the duration of the single slowest request.

The following sections present practical examples and examine potential issues that arise in each scenario.

## GIL
Python has traditionally employed the `GIL` (Global Interpreter Lock), which restricts execution to a single CPU core at any given moment, even when multiple cores are available. Whilst this simplifies memory management, the primary drawback concerns performance. A further consideration is whether existing synchronous code can be accelerated without a full rewrite.

## Bypassing the GIL in Python < 3.13
Where true parallel processing across multiple CPU cores is required, three principal options are available:
- **Use multiprocessing:** Rather than `threading`, the `multiprocessing` module spawns entirely separate Python processes, each with its own interpreter, memory space, and `GIL`.
- **Use C extensions:** Libraries such as `numpy`, `scipy`, and `pandas` perform heavy computation in C/C++, releasing the `GIL` during execution.
- **Use an alternative Python implementation:** PyPy, Jython, or IronPython handle execution differently, though they lack the full library ecosystem of CPython.

## Bypassing the GIL in Python >= 3.13
The CPython developers began work on a GIL-free solution with Python 3.13.

- **Python 3.13 (October 2024):** Experimental support was introduced. The standard distribution still enables the GIL by default; to run without it, the special free-threaded build must be explicitly installed or compiled (producing a `python3.13t` executable).
- **Python 3.14 (October 2025):** The free-threaded build progressed beyond experimental status to become officially supported, though it remains an optional download.
- **Long-term goal:** The Python Steering Council intends to make free-threaded (No-GIL) mode the default, removing the GIL from standard builds once third-party libraries have fully adapted.

These changes have significant implications for the use of `asyncio` with traditional synchronous Python code, as explored in the sections below.

## Practical Examples
### Verify the Installation
The following script confirms that `asyncio` is available in the current environment. Python 3.4 or newer is required. The examples in this section use Python 3.12.


```python
import sys

# Check asyncio version
print(f'Your asyncio version is tied to Python {sys.version.split()[0]}')
```

    Your asyncio version is tied to Python 3.12.12


### Initialise Runtime
As this article is presented in a Jupyter notebook, where an event loop is already running, the `nest_asyncio` library is used to patch and reuse the existing event loop.


```python
import asyncio
import time
import nest_asyncio

nest_asyncio.apply()
```

### Using Python 3.12

*standard synchronised code*


```python
def fetch_data_sync():
    print("Fetching data...")
    time.sleep(2)  # Simulate a delay in fetching data
    print("Data fetched successfully!")
    
def main():
    start_time = time.time()
    print("Starting the program...")
    fetch_data_sync()
    fetch_data_sync()
    fetch_data_sync()
    print("Program finished.")
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
    
main()
```

    Starting the program...
    Fetching data...
    Data fetched successfully!
    Fetching data...
    Data fetched successfully!
    Fetching data...
    Data fetched successfully!
    Program finished.
    Execution time: 6.001220464706421 seconds


As expected, the program ran for approximately 6 seconds. The following example converts the same logic to use native coroutines with `asyncio`.

*using asyncio*


```python
async def fetch_data_sync():
    print("Fetching data...")
    await asyncio.sleep(2)  # Simulate a delay in fetching data
    print("Data fetched successfully!")
    
async def main():
    start_time = time.time()
    print("Starting the program...")
    async with asyncio.TaskGroup() as tg:
        tg.create_task(fetch_data_sync())
        tg.create_task(fetch_data_sync())
        tg.create_task(fetch_data_sync())
    print("Program finished.")
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")

asyncio.run(main())
```

    Starting the program...
    Fetching data...
    Fetching data...
    Fetching data...
    Data fetched successfully!
    Data fetched successfully!
    Data fetched successfully!
    Program finished.
    Execution time: 2.002875328063965 seconds


As observed, the program completed in approximately 2 seconds. It should be noted, however, that the code required complete rewriting to use native coroutines. The following example examines what occurs when the original synchronous code is executed under `asyncio` without any modification.

*python code running under asyncio*


```python
async def fetch_data_sync():
    print("Fetching data...")
    time.sleep(2)  # Simulate a delay in fetching data
    print("Data fetched successfully!")
    
async def main():
    start_time = time.time()
    print("Starting the program...")
    async with asyncio.TaskGroup() as tg:
        tg.create_task(fetch_data_sync())
        tg.create_task(fetch_data_sync())
        tg.create_task(fetch_data_sync())
    print("Program finished.")
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")

asyncio.run(main())
```

    Starting the program...
    Fetching data...
    Data fetched successfully!
    Fetching data...
    Data fetched successfully!
    Fetching data...
    Data fetched successfully!
    Program finished.
    Execution time: 6.001770734786987 seconds


Execution returns to approximately 6 seconds. The changes applied have no effect; the code runs as though `asyncio` were absent. This demonstrates that a complete conversion to native coroutines is necessary in order to benefit from the `asyncio` event loop.

| **Synchronous code** | **Asynchronous equivalent** |
|---|---|
| `time.sleep(2)` | `await asyncio.sleep(2)` |
| `requests.get(url)` | `await httpx.AsyncClient().get(url)` or use `aiohttp` |
| `open('file.txt', 'r')` | `await aiofiles.open('file.txt', 'r')` |
| Standard database drivers | Async drivers or an ORM such as `SQLAlchemy` |

An alternative approach is to run synchronous tasks in a separate thread. The following example mixes synchronous tasks offloaded to threads with native coroutines, demonstrating how the two may be combined.

*run sync tasks in a separate thread*


```python
import asyncio
import time

def fetch_data_sync(loop_iteration):
    for i in range(int(loop_iteration) + 1):
        time.sleep(1)  # Simulate a delay in fetching data
    print("Sync data fetched successfully!")
    
async def fetch_data_async(loop_iteration):
    for i in range(int(loop_iteration) + 1):
        await asyncio.sleep(1)  # Simulate a delay in fetching data
    print("Async data fetched successfully!")
    
async def main():
    start_time = time.time()
    print("Starting the program...")
    async with asyncio.TaskGroup() as tg:
        tg.create_task(asyncio.to_thread(fetch_data_sync, 1))
        tg.create_task(fetch_data_async(2))
        tg.create_task(asyncio.to_thread(fetch_data_sync, 3))
        tg.create_task(fetch_data_async(4))
        tg.create_task(asyncio.to_thread(fetch_data_sync, 5))
        tg.create_task(fetch_data_async(6))
        tg.create_task(asyncio.to_thread(fetch_data_sync, 7))
        tg.create_task(fetch_data_async(8))
        tg.create_task(asyncio.to_thread(fetch_data_sync, 9))
        tg.create_task(fetch_data_async(10))
    print("Program finished.")
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    asyncio.run(main())
```

    Starting the program...
    Sync data fetched successfully!
    Async data fetched successfully!
    Sync data fetched successfully!
    Async data fetched successfully!
    Sync data fetched successfully!
    Async data fetched successfully!
    Sync data fetched successfully!
    Async data fetched successfully!
    Sync data fetched successfully!
    Async data fetched successfully!
    Program finished.
    Execution time: 11.00990891456604 seconds


The result of approximately 11 seconds is encouraging; however, this outcome reflects the use of a dummy sleep function. Since the CPU is idle during each sleep interval, there is ample time for the event loop to schedule other tasks. The following example replaces the sleep-based simulation with a genuinely CPU-intensive worker, calibrated to run for exactly 1 second.

*heavy workload without asyncio*


```python
def computational_heavy_1s_worker(task_id: str) -> int:
    """A pure CPU-bound mathematical loop that runs for exactly 1.0 second."""
    print(f"🔥 [{task_id}] CPU computation started (consuming 100% of its thread)...")
    
    start_time = time.perf_counter()
    dummy_accumulator = 0
    
    # This tight loop forces continuous CPU execution against a precise clock
    while time.perf_counter() - start_time < 1.0:
        # Performing continuous operations to keep the ALU (Arithmetic Logic Unit) busy
        dummy_accumulator += 1
            
    end_time = time.perf_counter()
    print(f"✅ [{task_id}] CPU computation finished in {end_time - start_time:.4f}s.")
    return dummy_accumulator

    
def main():
    start_time = time.time()
    print("Starting the program...")
    t1 = computational_heavy_1s_worker("1")
    t2 = computational_heavy_1s_worker("2")
    t3 = computational_heavy_1s_worker("3")
    t4 = computational_heavy_1s_worker("4")
    t5 = computational_heavy_1s_worker("5")
    t6 = computational_heavy_1s_worker("6")
    t7 = computational_heavy_1s_worker("7")
    t8 = computational_heavy_1s_worker("8")
    t9 = computational_heavy_1s_worker("9")
    t10 = computational_heavy_1s_worker("10")
    print("Program finished.")
    total_accumulator = t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8 + t9 + t10
    end_time = time.time()
    total_time = end_time - start_time
    acc_per_second = total_accumulator / total_time
    
    print("Total accumulator in milions: ", total_accumulator / 1_000_000, "M)")
    print(f"Execution time: {total_time} seconds")
    print(f"Accumulator per second: {acc_per_second / 1_000_000} M/s")
    
main()
```

    Starting the program...
    🔥 [1] CPU computation started (consuming 100% of its thread)...
    ✅ [1] CPU computation finished in 1.0000s.
    🔥 [2] CPU computation started (consuming 100% of its thread)...
    ✅ [2] CPU computation finished in 1.0000s.
    🔥 [3] CPU computation started (consuming 100% of its thread)...
    ✅ [3] CPU computation finished in 1.0000s.
    🔥 [4] CPU computation started (consuming 100% of its thread)...
    ✅ [4] CPU computation finished in 1.0000s.
    🔥 [5] CPU computation started (consuming 100% of its thread)...
    ✅ [5] CPU computation finished in 1.0000s.
    🔥 [6] CPU computation started (consuming 100% of its thread)...
    ✅ [6] CPU computation finished in 1.0000s.
    🔥 [7] CPU computation started (consuming 100% of its thread)...
    ✅ [7] CPU computation finished in 1.0000s.
    🔥 [8] CPU computation started (consuming 100% of its thread)...
    ✅ [8] CPU computation finished in 1.0000s.
    🔥 [9] CPU computation started (consuming 100% of its thread)...
    ✅ [9] CPU computation finished in 1.0000s.
    🔥 [10] CPU computation started (consuming 100% of its thread)...
    ✅ [10] CPU computation finished in 1.0000s.
    Program finished.
    Total accumulator in milions:  82.264652 M)
    Execution time: 10.001441478729248 seconds
    Accumulator per second: 8.2252795434496 M/s


The synchronous baseline produced approximately 82 million accumulator increments over 10 seconds, equivalent to roughly 8.2 million per second. The following example executes the same unmodified synchronous function via `asyncio.to_thread()`, with no changes to the worker code.

*heavy workload with asyncio using threads*


```python
def fetch_data(loop_iteration):
    print("Fetching data...")
    for i in range(int(loop_iteration) + 1):
        time.sleep(1)  # Simulate a delay in fetching data
        print(f"Loop iteration {i + 1} for task {loop_iteration}")
    print("Data fetched successfully!")
    
def computational_heavy_1s_worker(task_id: str) -> int:
    """A pure CPU-bound mathematical loop that runs for exactly 1.0 second."""
    print(f"🔥 [{task_id}] CPU computation started (consuming 100% of its thread)...")
    
    start_time = time.perf_counter()
    dummy_accumulator = 0
    
    # This tight loop forces continuous CPU execution against a precise clock
    while time.perf_counter() - start_time < 1.0:
        # Performing continuous operations to keep the ALU (Arithmetic Logic Unit) busy
        dummy_accumulator += 1
            
    end_time = time.perf_counter()
    print(f"✅ [{task_id}] CPU computation finished in {end_time - start_time:.4f}s.")
    return dummy_accumulator

    
async def main():
    start_time = time.time()
    print("Starting the program...")
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "1"))
        t2 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "2"))
        t3 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "3"))
        t4 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "4"))
        t5 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "5"))
        t6 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "6"))
        t7 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "7"))
        t8 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "8"))
        t9 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "9"))
        t10 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "10"))
    print("Program finished.")
    total_accumulator = t1.result() + t2.result() + t3.result() + t4.result() + t5.result() + t6.result() + t7.result() + t8.result() + t9.result() + t10.result()
    end_time = time.time()
    total_time = end_time - start_time
    acc_per_second = total_accumulator / total_time
    print("Total accumulator in millions: ", total_accumulator / 1_000_000, "M)")
    print(f"Execution time: {total_time} seconds")
    print(f"Accumulator per second: {acc_per_second / 1_000_000} M/s")
    
asyncio.run(main())
```

    Starting the program...
    🔥 [1] CPU computation started (consuming 100% of its thread)...
    🔥 [2] CPU computation started (consuming 100% of its thread)...
    🔥 [3] CPU computation started (consuming 100% of its thread)...
    🔥 [4] CPU computation started (consuming 100% of its thread)...
    🔥 [5] CPU computation started (consuming 100% of its thread)...
    🔥 [6] CPU computation started (consuming 100% of its thread)...
    🔥 [7] CPU computation started (consuming 100% of its thread)...
    🔥 [8] CPU computation started (consuming 100% of its thread)...
    🔥 [9] CPU computation started (consuming 100% of its thread)...
    🔥 [10] CPU computation started (consuming 100% of its thread)...
    ✅ [2] CPU computation finished in 1.0002s.
    ✅ [1] CPU computation finished in 1.0824s.
    ✅ [3] CPU computation finished in 1.0047s.
    ✅ [6] CPU computation finished in 1.0000s.
    ✅ [5] CPU computation finished in 1.0350s.
    ✅ [4] CPU computation finished in 1.0555s.
    ✅ [8] CPU computation finished in 1.0002s.
    ✅ [7] CPU computation finished in 1.0314s.
    ✅ [10] CPU computation finished in 1.0000s.
    ✅ [9] CPU computation finished in 1.0052s.
    Program finished.
    Total accumulator in millions:  12.727274 M)
    Execution time: 1.6391608715057373 seconds
    Accumulator per second: 7.7645057426905835 M/s


The program completed in approximately 1.6 seconds; however, only 12.7 million accumulator increments were produced, corresponding to approximately 7.77 million per second — marginally worse than the sequential baseline of 8.2 million per second. This indicates that raw computational throughput was lower under the threaded-asyncio approach than in the purely synchronous case. The explanation lies in the Python version: Python 3.12 still enforces the GIL, which prevents threads from executing Python bytecode in parallel. This approach nevertheless offers a clear advantage when combining synchronous and asynchronous code, even though it does not increase raw computational throughput.

### Using Python >= 3.13t
A Python interpreter version 3.13 or later with the free-threaded suffix `t` is required for the following examples. At the time of writing, the latest available free-threaded build was Python 3.14.7t, which is used for all subsequent benchmarks.

*check current asyncio version*


```python
import sys

# Check asyncio version
print(f'Your asyncio version is tied to Python {sys.version.split()[0]}')
```

    Your asyncio version is tied to Python 3.14.7


*initialise runtime*


```python
import asyncio
import time
import nest_asyncio

nest_asyncio.apply()
```

*heavy workload without asyncio*


```python
def computational_heavy_1s_worker(task_id: str) -> int:
    """A pure CPU-bound mathematical loop that runs for exactly 1.0 second."""
    print(f"🔥 [{task_id}] CPU computation started (consuming 100% of its thread)...")
    
    start_time = time.perf_counter()
    dummy_accumulator = 0
    
    # This tight loop forces continuous CPU execution against a precise clock
    while time.perf_counter() - start_time < 1.0:
        # Performing continuous operations to keep the ALU (Arithmetic Logic Unit) busy
        dummy_accumulator += 1
            
    end_time = time.perf_counter()
    print(f"✅ [{task_id}] CPU computation finished in {end_time - start_time:.4f}s.")
    return dummy_accumulator

    
def main():
    start_time = time.time()
    print("Starting the program...")
    t1 = computational_heavy_1s_worker("1")
    t2 = computational_heavy_1s_worker("2")
    t3 = computational_heavy_1s_worker("3")
    t4 = computational_heavy_1s_worker("4")
    t5 = computational_heavy_1s_worker("5")
    t6 = computational_heavy_1s_worker("6")
    t7 = computational_heavy_1s_worker("7")
    t8 = computational_heavy_1s_worker("8")
    t9 = computational_heavy_1s_worker("9")
    t10 = computational_heavy_1s_worker("10")
    print("Program finished.")
    total_accumulator = t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8 + t9 + t10
    end_time = time.time()
    total_time = end_time - start_time
    acc_per_second = total_accumulator / total_time
    
    print("Total accumulator in milions: ", total_accumulator / 1_000_000, "M)")
    print(f"Execution time: {total_time} seconds")
    print(f"Accumulator per second: {acc_per_second / 1_000_000} M/s")
    
main()
```

    Starting the program...
    🔥 [1] CPU computation started (consuming 100% of its thread)...
    ✅ [1] CPU computation finished in 1.0000s.
    🔥 [2] CPU computation started (consuming 100% of its thread)...
    ✅ [2] CPU computation finished in 1.0000s.
    🔥 [3] CPU computation started (consuming 100% of its thread)...
    ✅ [3] CPU computation finished in 1.0000s.
    🔥 [4] CPU computation started (consuming 100% of its thread)...
    ✅ [4] CPU computation finished in 1.0000s.
    🔥 [5] CPU computation started (consuming 100% of its thread)...
    ✅ [5] CPU computation finished in 1.0000s.
    🔥 [6] CPU computation started (consuming 100% of its thread)...
    ✅ [6] CPU computation finished in 1.0000s.
    🔥 [7] CPU computation started (consuming 100% of its thread)...
    ✅ [7] CPU computation finished in 1.0000s.
    🔥 [8] CPU computation started (consuming 100% of its thread)...
    ✅ [8] CPU computation finished in 1.0000s.
    🔥 [9] CPU computation started (consuming 100% of its thread)...
    ✅ [9] CPU computation finished in 1.0000s.
    🔥 [10] CPU computation started (consuming 100% of its thread)...
    ✅ [10] CPU computation finished in 1.0000s.
    Program finished.
    Total accumulator in milions:  62.859276 M)
    Execution time: 10.001799583435059 seconds
    Accumulator per second: 6.284796598414879 M/s


The synchronous baseline on the Python 3.14.7t interpreter produced approximately 63 million accumulator increments over 10 seconds, equivalent to roughly 6.3 million per second. This is significantly lower than the Python 3.12 result, which is attributable to the additional overhead introduced by the free-threaded runtime. The following example executes the same unmodified synchronous function via `asyncio.to_thread()`, as before.

*heavy workload with asyncio using threads*


```python
def fetch_data(loop_iteration):
    print("Fetching data...")
    for i in range(int(loop_iteration) + 1):
        time.sleep(1)  # Simulate a delay in fetching data
        print(f"Loop iteration {i + 1} for task {loop_iteration}")
    print("Data fetched successfully!")
    
def computational_heavy_1s_worker(task_id: str) -> int:
    """A pure CPU-bound mathematical loop that runs for exactly 1.0 second."""
    print(f"🔥 [{task_id}] CPU computation started (consuming 100% of its thread)...")
    
    start_time = time.perf_counter()
    dummy_accumulator = 0
    
    # This tight loop forces continuous CPU execution against a precise clock
    while time.perf_counter() - start_time < 1.0:
        # Performing continuous operations to keep the ALU (Arithmetic Logic Unit) busy
        dummy_accumulator += 1
            
    end_time = time.perf_counter()
    print(f"✅ [{task_id}] CPU computation finished in {end_time - start_time:.4f}s.")
    return dummy_accumulator

    
async def main():
    start_time = time.time()
    print("Starting the program...")
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "1"))
        t2 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "2"))
        t3 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "3"))
        t4 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "4"))
        t5 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "5"))
        t6 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "6"))
        t7 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "7"))
        t8 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "8"))
        t9 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "9"))
        t10 = tg.create_task(asyncio.to_thread(computational_heavy_1s_worker, "10"))
    print("Program finished.")
    total_accumulator = t1.result() + t2.result() + t3.result() + t4.result() + t5.result() + t6.result() + t7.result() + t8.result() + t9.result() + t10.result()
    end_time = time.time()
    total_time = end_time - start_time
    acc_per_second = total_accumulator / total_time
    print("Total accumulator in millions: ", total_accumulator / 1_000_000, "M)")
    print(f"Execution time: {total_time} seconds")
    print(f"Accumulator per second: {acc_per_second / 1_000_000} M/s")
    
asyncio.run(main())
```
```
Starting the program...
🔥 [1] CPU computation started (consuming 100% of its thread)...
🔥 [2] CPU computation started (consuming 100% of its thread)...
🔥 [3] CPU computation started (consuming 100% of its thread)...
🔥 [4] CPU computation started (consuming 100% of its thread)...
🔥 [5] CPU computation started (consuming 100% of its thread)...
🔥 [6] CPU computation started (consuming 100% of its thread)...
🔥 [7] CPU computation started (consuming 100% of its thread)...
🔥 [8] CPU computation started (consuming 100% of its thread)...
🔥 [9] CPU computation started (consuming 100% of its thread)...
🔥 [10] CPU computation started (consuming 100% of its thread)...
✅ [1] CPU computation finished in 1.0000s.
✅ [2] CPU computation finished in 1.0000s.
✅ [3] CPU computation finished in 1.0000s.
✅ [5] CPU computation finished in 1.0000s.
✅ [4] CPU computation finished in 1.0005s.
✅ [6] CPU computation finished in 1.0000s.
✅ [7] CPU computation finished in 1.0000s.
✅ [8] CPU computation finished in 1.0000s.
✅ [9] CPU computation finished in 1.0000s.
✅ [10] CPU computation finished in 1.0000s.
Program finished.
Total accumulator in millions:  27.389394 M)
Execution time: 1.1771600246429443 seconds
Accumulator per second: 23.26734974567943 M/s
```

The results show 27 million accumulator increments produced in 1.18 seconds, yielding approximately 23.3 million per second — representing a nearly threefold improvement over the Python 3.12 result, where the GIL serialised thread execution.

### Using threads safely by asyncio.to_thread()

It is generally safe to run different Python methods using `asyncio.to_thread()`, but it depends heavily on your Python version and whether those methods modify shared data or not.

In modern Python >= 3.13t, the rules for threading changed dramatically due to the introduction of free-threaded Python without the GIL. There are still some issues we must bear in mind to keep our code thread-safe.

1. **Pure calculation and read-only tasks ( always safe ):** If the different methods only calculate data, read local variables, or perform network I/O, it is 100% safe. Because `asyncio.to_thread() automatically grabs an isolated worker thread from an internal thread pool, running independent methods side-by-side will not cause conflicts.
2. **Modifying global data or shared objects ( dangerous ):** If our methods try to modify the same global variable, list, dictionary, database object etc., at the same time, we will encounter data corruption or race conditions.
    - older Python (with GIL): The GIL protects Python's internal memory, but your application logic can still break if two threads try to update a dictionary key simultaneously.
    - free-threaded Python: Without the GIL, threads can execute true concurrent modifications. Modifying unprotected custom objects or global states simultaneously will crash or corrupt data.

*dangerous way*
```
shared_counter = 0

def increment_score():
    global shared_counter
    # DANGEROUS: Multiple threads modifying the same integer simultaneously
    for _ in range(100_000):
        shared_counter += 1 

async def main():
    async with asyncio.TaskGroup() as tg:
        # Running these concurrently via threads can cause incorrect totals
        tg.create_task(asyncio.to_thread(increment_score))
        tg.create_task(asyncio.to_thread(increment_score))

asyncio.run(main())
```

*safe way*
```
import threading

shared_counter = 0
data_lock = threading.Lock() # Use a THREAD lock, not an asyncio lock!

def safe_increment_score():
    global shared_counter
    for _ in range(100_000):
        # Only one thread can modify the counter at a microsecond
        with data_lock:
            shared_counter += 1
```

## Conclusion

Throughout this article we have explored the relationship between `asyncio` and traditional synchronous Python code across different interpreter versions and workload types. The key findings can be summarised as follows.

**asyncio excels at I/O-bound concurrency.** When tasks spend most of their time waiting — for network responses, database queries, or file reads — rewriting those tasks to be `async` and using `await`-compatible libraries (such as `httpx`, `aiohttp`, or `aiofiles`) produces dramatic improvements. In our benchmark, three simulated I/O tasks that originally ran sequentially in approximately 6 seconds completed in just 2 seconds once converted to proper async code using `asyncio.TaskGroup`.

**Wrapping unmodified synchronous code in asyncio does not help I/O tasks.** Placing a blocking `time.sleep()` call inside a coroutine without converting it to `await asyncio.sleep()` yields no benefit — execution remains strictly sequential. The event loop cannot yield control during a blocking call, so the full sequential duration is preserved.

**`asyncio.to_thread()` unlocks concurrency for unmodified synchronous code.** By offloading blocking functions to a thread pool, `asyncio.to_thread()` allows multiple synchronous tasks to overlap in time. This is particularly valuable when migrating legacy codebases incrementally or when using third-party libraries that have no async counterpart.

**CPU-bound tasks require the free-threaded interpreter.** Under the standard CPython interpreter (Python 3.12 and earlier), the GIL prevents threads from executing Python bytecode in parallel. Running CPU-bound work through `asyncio.to_thread()` on Python 3.12 achieved a wall-clock speedup but delivered *worse* total throughput (~7.77 M/s versus ~8.2 M/s) because threads contended for the GIL. Switching to the free-threaded build (Python 3.14.7t, suffix `t`) raised throughput to approximately 23.3 M/s — nearly a threefold improvement — because all worker threads could now execute Python code simultaneously on separate CPU cores.

**Thread safety becomes the programmer's responsibility without the GIL.** Once the GIL is removed, shared mutable state must be protected explicitly. Any function that writes to a global variable, list, or dictionary from multiple threads simultaneously must use a `threading.Lock`. Read-only and pure-computation tasks remain unconditionally safe.

**Choosing the right tool for the job:**

| Scenario | Recommended approach |
|---|---|
| I/O-bound with async-compatible libraries | Native `async`/`await` with `asyncio` |
| I/O-bound with legacy synchronous libraries | `asyncio.to_thread()` |
| CPU-bound on Python <= 3.12 | `multiprocessing` (bypasses the GIL entirely) |
| CPU-bound on Python >= 3.13 t | `asyncio.to_thread()` or `threading` |
| Shared mutable state across threads | Always protect with `threading.Lock` |

As the Python ecosystem continues to mature around the free-threaded interpreter, the boundary between async and threaded programming will blur further. For now, understanding which version of the interpreter you are targeting — and whether your bottleneck is I/O latency or raw CPU throughput — is the most important decision you can make before reaching for `asyncio`.

Further reading on the `asyncio` library is available in the official Python documentation at [docs.python.org/3/library/asyncio.html](https://docs.python.org/3/library/asyncio.html).

Did this article help you? Let me know in the comments below, and don't forget to drop a like if you enjoyed the read! Thank you.
