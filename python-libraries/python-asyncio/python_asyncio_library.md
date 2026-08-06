# Python Asyncio Library
Asyncio is a built-in Python library available from Python 3.4 onwards, used to write concurrent programmes with the async and await syntax. Unlike multithreading or multiprocessing, asyncio achieves concurrency within a single thread through an architecture known as an **event loop**. It is particularly well suited to I/O-bound tasks, where execution time is dominated by waiting for external responses, such as fetching data from web APIs, querying databases, or reading network streams.

## How it works - cooperative multitasking
In standard sequential code, if a programme requests data from a website, the entire application blocks until the server responds.

Asyncio uses cooperative multitasking. When a task reaches a waiting point, such as an API request, it voluntarily pauses and yields control back to the **event loop**. The event loop then switches to another task that is ready to run. When the external response arrives, the event loop resumes the original task so that it can complete its work.

## Core building blocks
We rely on three primary components:
- **Coroutines:** Functions defined with `async def`. Calling them does not execute the code immediately; instead, it returns a coroutine object that must be awaited to run.
- **The await keyword:** Placed before an operation to pause the coroutine temporarily, allowing the event loop to process other tasks.
- **Event loop:** The central coordinator that manages and switches between running asynchronous tasks. It is started with `asyncio.run()`.

## Practical examples

### Verify the installation
The following script can be used to confirm that asyncio is available in the environment. Python 3.4 or newer is required.


```python
import sys

# Check asyncio version
print(f'Your asyncio version is tied to Python {sys.version.split()[0]}')
```

    Your asyncio version is tied to Python 3.12.12


### Basics of async and await
We use `async def` to define a coroutine and `await` to pause execution without blocking the event loop. Because this article is presented in a Jupyter notebook, where an event loop is already running, we need to use the `nest_asyncio` library to reuse the existing event loop.

*Initialise the runtime*


```python
import asyncio
import time
import nest_asyncio

nest_asyncio.apply()
```


*Basic code example*


```python
async def fetch_data(id, delay):
    print(f"Task {id}: Fetching data...")
    # Simulate a network delay without blocking the whole program
    await asyncio.sleep(delay)  
    print(f"Task {id}: Data received!")
    return f"Result {id}"

async def main():
    start_time = time.time()
    # Schedule and run both tasks at the same time
    task1 = asyncio.create_task(fetch_data(1, 2))
    task2 = asyncio.create_task(fetch_data(2, 3))
    
    # Wait for both to finish
    await task1
    await task2
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time} seconds")

# Start the Event Loop
asyncio.run(main()) 
 
```

    Task 1: Fetching data...
    Task 2: Fetching data...
    Task 1: Data received!
    Task 2: Data received!
    Total execution time: 3.0017387866973877 seconds


### Sequential vs concurrent execution
Awaiting coroutines one by one is sequential, whereas `asyncio.gather()` runs them concurrently. A standard Python list does not create concurrency, even when the `await` keyword is used.


```python
async def work(name, delay):
    print(f"Task {name}: Starting work...")
    await asyncio.sleep(delay)
    print(f"Task {name}: Work completed!")
    
async def run_sequentially():
    start_time = time.time()
    result = [
        await work("A", 2),
        await work("A", 2),
        await work("B", 3)
    ]
    print("Sequential:", result)
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:2f} seconds")
    
async def run_concurrently():
    start_time = time.time()
    result = await asyncio.gather(
        work("A", 2),
        work("A", 2),
        work("B", 3)
    )
    print("Concurrent:", result)
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:2f} seconds")
    
async def main():
    print("Running tasks sequentially...")
    await run_sequentially()
    
    print("\nRunning tasks concurrently...")
    await run_concurrently()

# Start the Event Loop
asyncio.run(main())
```

    Running tasks sequentially...
    Task A: Starting work...
    Task A: Work completed!
    Task A: Starting work...
    Task A: Work completed!
    Task B: Starting work...
    Task B: Work completed!
    Sequential: [None, None, None]
    Total execution time: 7.006525 seconds
    
    Running tasks concurrently...
    Task A: Starting work...
    Task A: Starting work...
    Task B: Starting work...
    Task A: Work completed!
    Task A: Work completed!
    Task B: Work completed!
    Concurrent: [None, None, None]
    Total execution time: 3.002129 seconds


### Create background tasks
We use `asyncio.create_task()` when we want a coroutine to begin executing immediately in the background.


```python
async def ticker(name, count):
    for i in range(count):
        await asyncio.sleep(1)
        print(f"{name}: Tick {i + 1}")
        
async def main():
    task1 = asyncio.create_task(ticker("Ticker 1", 5))
    task2 = asyncio.create_task(ticker("Ticker 2", 3))
    print("Both tickers are running concurrently...")
    start_time = time.time()
    await task1
    await task2
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:2f} seconds")
    
asyncio.run(main())
```

    Both tickers are running concurrently...
    Ticker 1: Tick 1
    Ticker 2: Tick 1
    Ticker 1: Tick 2
    Ticker 2: Tick 2
    Ticker 1: Tick 3
    Ticker 2: Tick 3
    Ticker 1: Tick 4
    Ticker 1: Tick 5
    Total execution time: 5.004832 seconds


### Waiting with a timeout
We wrap an awaitable with `asyncio.wait_for()` to raise an error if it takes too long.


```python
async def slow_operation():
    await asyncio.sleep(2)
    return "Slow operation completed"

async def main():
    start = time.time()
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=1)
        print(result)
    except asyncio.TimeoutError:
        print("The operation timed out!")
    finally:
        result = await asyncio.wait_for(slow_operation(), timeout=3)
        print(result)
        end = time.time()
    print(f"Total execution time: {end - start:2f} seconds")
    
asyncio.run(main())
```

    The operation timed out!
    Slow operation completed
    Total execution time: 3.003181 seconds


### Producer-consumer with `asyncio.Queue`
A queue is useful when one part of a programme produces work and another part consumes it.


```python
async def producer(queue):
    for i in range(5):
        await asyncio.sleep(1)  # Simulate a delay in producing
        item = f"item-{i}"
        await queue.put(item)
        print(f"Produced {item}")
        
async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:  # Check for the sentinel value to exit
            queue.task_done()
            break
        await asyncio.sleep(2)  # Simulate a delay in consuming
        print(f"Consumed {item}")
        queue.task_done()
        
async def main():
    start_time = time.time()
    queue = asyncio.Queue()
    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))
    await producer_task
    await queue.put(None)  # Send the sentinel value to the consumer
    await consumer_task
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:2f} seconds")
    
asyncio.run(main())
```

    Produced item-0
    Produced item-1
    Consumed item-0
    Produced item-2
    Produced item-3
    Consumed item-1
    Produced item-4
    Consumed item-2
    Consumed item-3
    Consumed item-4
    Total execution time: 11.011405 seconds


Based solely on the sleep durations, this task would take around 15 seconds, but using `asyncio.Queue` reduces this to 11 seconds.

### Limit concurrency with Semaphore
A semaphore limits how many coroutines may enter a critical section at the same time.


```python
async def fetch(item, semaphore):
    async with semaphore:
        print(f"Fetching {item}...")
        await asyncio.sleep(2)  # Simulate a network delay
        print(f"Fetched {item}!")
        return item * 10
    
async def main():
    start_time = time.time()
    semaphore = asyncio.Semaphore(3)  # Limit to 3 concurrent fetches
    items = [1, 2, 3, 4, 5]
    tasks = [asyncio.create_task(fetch(item, semaphore)) for item in items]
    results = await asyncio.gather(*tasks)
    print(f"Results: {results}")
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:2f} seconds")

asyncio.run(main())
```

    Fetching 1...
    Fetching 2...
    Fetching 3...
    Fetched 1!
    Fetched 2!
    Fetched 3!
    Fetching 4...
    Fetching 5...
    Fetched 4!
    Fetched 5!
    Results: [10, 20, 30, 40, 50]
    Total execution time: 4.004785 seconds


The process in this example is as follows:
1. fetch the first 3 coroutines
2. process them
3. wait for 2 seconds
4. fetch the final 2 coroutines
5. process them
6. wait for 2 seconds

Total time: 4 seconds

### Async generators
An async generator is a function defined with `async def` that uses the `yield` keyword. It allows execution to pause, emit a value, and await asynchronously before producing the next item.


```python
async def async_number_generator(limit):
    for i in range(limit):
        await asyncio.sleep(1)  # Simulate some delay
        yield i
        
async def main():
    async for number in async_number_generator(5):
        print(f"Generated number: {number}")

asyncio.run(main())
```

    Generated number: 0
    Generated number: 1
    Generated number: 2
    Generated number: 3
    Generated number: 4


### Async iterators
An async iterator is an object, usually a class, that implements two specific magic methods: `__aiter__()` and `__anext__()`. You generally need to implement this manually only when creating complex custom data structures or SDKs.
- `__aiter__()`: Must return the iterator object itself.
- `__anext__()`: An async method that returns the next value, or raises `StopAsyncIteration` to terminate the loop.

An iterator can be implemented in much the same way as the previous generator.


```python
class AsyncNumberGenerator:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.current < self.limit:
            await asyncio.sleep(1)  # Simulate some delay
            value = self.current
            self.current += 1
            return value
        else:
            raise StopAsyncIteration
        
async def main():
    async for number in AsyncNumberGenerator(5):
        print(f"Generated number: {number}")

asyncio.run(main())
```

    Generated number: 0
    Generated number: 1
    Generated number: 2
    Generated number: 3
    Generated number: 4


### Handle cancellation
Tasks can be cancelled. Catch `asyncio.CancelledError` when cleanup is required.


```python
async def worker():
    try:
        while True:
            print("Worker is working...")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Worker has been cancelled.")
        raise
    
async def main():
    task = asyncio.create_task(worker())
    await asyncio.sleep(3)  # Let the worker run for a while
    task.cancel()  # Cancel the worker
    try:
        await task
    except asyncio.CancelledError:
        print("Main: Worker task has been cancelled.")

asyncio.run(main())
```

    Worker is working...
    Worker is working...
    Worker is working...
    Worker has been cancelled.
    Main: Worker task has been cancelled.


### Structured concurrency with TaskGroup

In Python 3.11 and later, `TaskGroup` provides a cleaner way to manage related tasks together. Before `TaskGroup`, developers commonly used `asyncio.gather()`, but there is a significant limitation: if one task fails, the others continue running, which can lead to silent failures or leaked resources. `TaskGroup` addresses this problem.

3 core benefits:
- **All or nothing:** If any task inside a `TaskGroup` raises an unhandled exception, the group immediately issues a cancellation request for the remaining running tasks. This helps prevent orphaned tasks from continuing in the background.
- **Exception groups (`ExceptionGroup`):** If multiple tasks fail at the same time, `TaskGroup` does not report only the first error. Instead, it collects every error and raises them together as an `ExceptionGroup`, a Python 3.11 feature.
- **Automatic awaiting:** You do not need to manually track and await a list of tasks. When execution reaches the end of the `with` block, Python automatically waits for every task in the group to finish before continuing.


```python
async def job(name, duration):
    print(f"Job {name} started, will take {duration} seconds.")
    await asyncio.sleep(duration)
    print(f"Job {name} completed.")
    
async def main():
    start_time = time.time()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(job("A", 2))
        tg.create_task(job("B", 3))
        tg.create_task(job("C", 1))
    print("All jobs completed.")
    end_time = time.time()
    print(f"Total time: {end_time - start_time} seconds.")
    
asyncio.run(main())
```

    Job A started, will take 2 seconds.
    Job B started, will take 3 seconds.
    Job C started, will take 1 seconds.
    Job C completed.
    Job A completed.
    Job B completed.
    All jobs completed.
    Total time: 3.002323627471924 seconds.


### Low-level micromanagement with `asyncio.wait`
`asyncio.wait()` is a low-level function used to monitor a collection of already created background tasks. Unlike higher-level tools such as `asyncio.TaskGroup` or `asyncio.gather()`, it does not return the results of the tasks. Instead, it pauses execution and returns two sets: completed and pending tasks.

*Basic example*


```python
async def job(name, duration):
    print(f"Job {name} started, will take {duration} seconds.")
    await asyncio.sleep(duration)
    print(f"Job {name} completed.")
    return f"Result of job {name}"
    
async def main():
    tasks = [
        asyncio.create_task(job("A", 2)),
        asyncio.create_task(job("B", 3)),
        asyncio.create_task(job("C", 1))
    ]
    
    done, _ = await asyncio.wait(tasks)
    
    for task in done:
        print(f"Completed: {task.result()}")
    
asyncio.run(main())
```

    Job A started, will take 2 seconds.
    Job B started, will take 3 seconds.
    Job C started, will take 1 seconds.
    Job C completed.
    Job A completed.
    Job B completed.
    Completed: Result of job C
    Completed: Result of job A
    Completed: Result of job B


### Using `asyncio.wait` with the `return_when` argument
The real value of `asyncio.wait()` lies in its `return_when` argument. This allows you to stop waiting early based on three distinct behaviours.
- `asyncio.ALL_COMPLETED` (default): The function waits until every task in the set has completed. No tasks remain pending.
- `asyncio.FIRST_COMPLETED`: Returns when the first task finishes. This is useful when you are querying multiple servers and only need the first response.
- `asyncio.FIRST_EXCEPTION`: Returns immediately if any task raises an error.



```python
async def job(name, duration):
    print(f"Job {name} started, will take {duration} seconds.")
    await asyncio.sleep(duration)
    print(f"Job {name} completed.")
    return f"Result of job {name}"
    
async def main():
    tasks = [
        asyncio.create_task(job("A", 2)),
        asyncio.create_task(job("B", 3)),
        asyncio.create_task(job("C", 1))
    ]
    
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    
    for task in done:
        print(f"Completed: {task.result()}")
    
    for task in pending:
        task.cancel()
        print(f"Cancelled: {task}")

asyncio.run(main())
```

    Job A started, will take 2 seconds.
    Job B started, will take 3 seconds.
    Job C started, will take 1 seconds.
    Job C completed.
    Completed: Result of job C
    Cancelled: <Task cancelling name='Task-71' coro=<job() running at /tmp/ipykernel_147702/562934988.py:3> wait_for=<Future cancelled>>
    Cancelled: <Task cancelling name='Task-70' coro=<job() running at /tmp/ipykernel_147702/562934988.py:3> wait_for=<Future cancelled>>


### Using `asyncio.wait` with the `timeout` argument
You can pass a timeout value, in seconds, to a group of tasks to prevent your application from hanging indefinitely.



```python
async def job(name, duration):
    print(f"Job {name} started, will take {duration} seconds.")
    await asyncio.sleep(duration)
    print(f"Job {name} completed.")
    return f"Result of job {name}"
    
async def main():
    tasks = [
        asyncio.create_task(job("A", 2)),
        asyncio.create_task(job("B", 3)),
        asyncio.create_task(job("C", 1))
    ]
    
    # Stop waiting after 1.5 seconds
    done, pending = await asyncio.wait(tasks, timeout=1.5)

    print(f"Finished on time: {len(done)}")
    print(f"Still running in background: {len(pending)}")

    # Crucial: Clean up or cancel pending tasks if you don't want them leaking!
    for task in pending:
        task.cancel()
        print(f"Cancelled: {task}")

asyncio.run(main())

```

    Job A started, will take 2 seconds.
    Job B started, will take 3 seconds.
    Job C started, will take 1 seconds.
    Job C completed.
    Finished on time: 1
    Still running in background: 2
    Cancelled: <Task cancelling name='Task-78' coro=<job() running at /tmp/ipykernel_147702/125214506.py:3> wait_for=<Future cancelled>>
    Cancelled: <Task cancelling name='Task-77' coro=<job() running at /tmp/ipykernel_147702/125214506.py:3> wait_for=<Future cancelled>>


You can combine both parameters. However, `return_when` does not automatically cancel pending tasks, whereas `timeout` leaves them running unless you cancel them explicitly. For that reason, it is generally better to call `task.cancel()` on pending tasks.

## Conclusion
In this article, we explored how `asyncio` helps you structure efficient, non-blocking Python programmes by coordinating many tasks within a single event loop. We covered the core building blocks, including coroutines, task creation, and orchestration patterns such as `asyncio.gather()` and `asyncio.wait()`.

The main practical takeaway is that concurrency is not only about speed but also about control: you decide when to wait, when to continue, and how to handle partial completion, failure, and cancellation safely. In particular, when using timeouts, you should clean up unfinished tasks explicitly to avoid background task leakage.

With these patterns, you now have a reliable foundation for real-world asynchronous applications such as network clients, API integrations, and data pipelines. The next step is to apply the same principles with proper exception handling, structured cancellation, and observability so that your asynchronous code remains both fast and maintainable at scale.

Did this article help you? Let me know in the comments below, and don't forget to drop a like if you enjoyed the read! Thank you.
