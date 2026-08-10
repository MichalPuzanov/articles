# Asyncio Using Traditional Python Code

## Introduction
In this article we are going to benchmark using Python library `asyncio` with traditional Python code in different enviroments. We know that `asyncio` is very good to use with Python libraries which support asynchronous programming. It really helps when we can work asynchronously when we fetch data from different sources or wait for hardware responses. Basically ever time our application hits a bottleneck caused by network latency, third-party server responces or heavy database communication. `asyncio` allows single thread to handle thousands of active operations at the same time. It is fantastic tool which can help as forexample with:
- **High-performance web scrapers and crawlers:** `asyncio` lets you fire off hundreds of web requests at once using async libraries like httpx or aiohttp. The program sits back, monitors the event loop, and processes each webpage the exact millisecond its data finishes downloading.
- ** Real-time chat apps and websocket servers:** Instead of creating 5,000 heavy operating system threads (which would completely overwhelm your computer's memory), `asyncio` maintains all 5,000 connections inside a single thread. It consumes almost no idle CPU power while waiting for incoming chat messages.
- **Discord bots, telegram bots, slack integration:** Popular framework libraries are built directly on top of `asyncio`. A single bot instance can listen for events across thousands of servers simultaneously without dropping any incoming commands.
- **Microservices and API aggregators like FastAPI:** Using tools like asyncio.TaskGroup inside a FastAPI gateway service, you can query the database and the two external APIs concurrently. The total response time drops from the sum of all three delays down to the time of whichever single request takes the longest. 

Today we are going to see examples and possible solutions for issues with them.

## GIL 
Python was traditionally used `GIL` - Global Interpreter Lock. Even our environment is offering multiple CPU cores, we are still able to use just one. Of course it is making our life easier, but major issue is performance of our code. Another issue is that we can have some traditional Python synchronised code, can we make it faster ?

## Bypass the GIL Python < 3.13
If we need true parallel processing across multiple CPU cores, we have three primary options:
- **Use multiprocessing:** Instead of `treading`, we use the multiprocessing module. This spawns entirely separate Python processes, each with its own interpreter, memory spacen and `GIL`.
- **Use C-extensions:** Libraties like `numpy`, `scipy`, `pandas` do they heavy computing in C/C++, which releases the `GIL` during execution.
- **Use an alternative Python:** PyPy, Jython, or IronPython handle execution differently, though they lack the full library ecosysten of CPython. 

## Bypass the GIL Python => 3.13
The developers of CPython (standard Python interpreter), started to work on "no GIL" solution first in Python version 3.13.

- **Python 3.13 (October 2024):** Introduced Experimental Support. The standard download still uses the GIL by default. To run without it, you must explicitly install or compile the special "free-threaded" build (which creates a python3.13t executable).
- **Python 3.14 (October 2025):** The free-threaded build moved beyond experimental status to become Officially Supported but remains an optional download.
- **Future Long-Term Goal:** The Python Steering Council plans to eventually make the free-threaded (No-GIL) mode the default option, completely removing the GIL from standard builds once third-party libraries have fully adapted.

This will affect significantly using `asyncio` even with our traditional Python sychronous code. Let's continue with practical coding.

## Practical examples
### Verify the installation
The following script can be used to confirm that asyncio is available in the environment. Python 3.4 or newer is required. We are now running Python version 3.12.


```python
import sys

# Check asyncio version
print(f'Your asyncio version is tied to Python {sys.version.split()[0]}')
```

    Your asyncio version is tied to Python 3.12.12


### Initialise runtime
Because this article is presented in a Jupyter notebook, where an event loop is already running, we need to use the `nest_asyncio` library to reuse the existing event loop.


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


As we expected program took roughly 6 seconds. Now we are going to change the code to asynchronous and use `asyncio`.

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


As we can see know program took roughly 2 seconds. Wow it is fantastic, but bear in mind we needed to rebuild the code to make it asynchronous. Now let's have a look what would happen if we don't change original code and run it under `asyncio`.

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


We are back to 6 seconds. All that changes we did, don't have any effect, the code is running like there is no `asyncio`. So basically it means we need to all our code change to asynchronous if we need use `asyncio` advantage.

| **normal synchronous code** | **asynchronous equivalent** | 
|-----------------------------|-----------------------------|
| `time.sleep(2)` | `await asyncio.sleep(2)` |
| `requests.get(url)` | `await httpx.AsincClient().get(url)` or use `aiohttp` |
| `open('file.txt', 'r')` | `await aiofiles.open('file.txt', 'r')` |
| standard database drivers | async drivers or orm like `SQLAlchemy` |

The solution for that is to run synchronous tasks in different thread. Our code runs sleep for 1 second roughly 50 times, but final time is much less no matter if we run sync or async method.

*run sync tasks in different thread*


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


The result is 11 seconds, it looks fantastic ! Sort of, because we are using dummy sleep function. It means CPU doesn't do anything, just sleep and there is plenty of time to run another task. Let's replace our dummy sleep method with heavy computing time method. Tge method should last exactly 1 second to run.

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


We ran synchronous code, there were 82 million accumulators created in 10 seconds, so it means roughly 8.2 millions per second. Now we are going to run it using threads. Remember no change to code, still using synchronous code, just run it under asyncio.

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


Wow it's fantastic, it ran just 1.6 second, but wait the moment, it created just 12.7 millions accumulators, which means 7.77 million accumulators per second. The final performance was worse then in previous synchronised example! So if it runs 10 secounds it will create less total accumulators, it means computer power is smaller in asynchronous that synchronous? It's version of Python we have, we are doing that test on 3.12., but there is GIL. Still this solution has very good advantage if you want to use synchronous and asynchronous code together, but doesn't bring any computing power.

### Using Python =>3.13 t
We need to use Python interpreter =>3.13, and it needs to be with suffix `t` . In time of writing the latest available version which support threads was 3.14.7t. So we are going to use it now for our code.

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


We ran synchronous code, in Python 3.14.7t interpreter. There were 63 million accumulators created in 10 seconds, so it means roughly 6.3 millions per second. This significantly lower than in Python 3.12 interpreter. Now we are going to run it using threads. Remember no change to code, still using synchronous code, just run it under asyncio.

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

We can see now these values: 27 millions of acummulators, in 1.18 seconds, 23.3 million accumulators per second, it is almost 3 times more using threads in Python interpreter 3.14.7t than in old 3.12.12 where GIL was in charge.

### Using threads safely by asyncio.to_thread()

It is generally safe to run different Python methods using `asyncio.to_thread()`, but it depends heavily on your Python version and whether those methods modify shared data or not.

In modern Python >= 3.13 t, the rules for threading changed dramatically due to introduction of free-threaded Python without GIL. There are still some issues we have bear in mind to keep our code thread-safe.

1. **Pure calculation and read-only tasks ( always safe ):** If the different methods only calculate data, read local variables, or perform network I/O, it is 100% safe. Because `asyncio.to_thread() automatically grabs an isolated worker thread from an internal thread pool, running independent methods side-by-side will not cause conflicts.
2. **Modifying global data or shared objects ( dangerous ):** If our methods try to modify the same global variable, list, dictionary, database object etc., at the same time, we will encounter data corruption or race conditions.
    - older Python (with GIL): The GIL protects Python's internal memory, but your application logic can still break if two threads try to update a dictionary key simultaneously.
    - free-threaded Python: Without GIL, threads can execute true concurrent modifications. Modifiying unprotected custom objects or global states sumultaneously will crash or corrupt data.

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

Did this article help you? Let me know in the comments below, and don't forget to drop a like if you enjoyed the read! Thank you.
