
# RabbitMQ + Pika Thread Safety Benchmark Demo

This lab demonstrates:

1. Sync producer with Pika
2. Multithreading using a shared channel (unsafe)
3. Fix using threading.Lock()
4. Benchmark results comparison

---

# Prerequisites

Virtual env:

python -m venv .env

source .env/bin/activate

Install dependency:

pip install pika

Run RabbitMQ:

docker run -d --name rabbit  -p 5672:5672  -p 15672:1..5672  rabbitmq:3-management

Management UI:
http://localhost:15672
guest / guest

---

# Step 1: Create queue

python setup_queue.py

Expected output:
Queue created successfully

---

# Step 2: Run Sync Benchmark

python sync_producer.py

Example output:

SYNC RESULT
Messages: 20000
Time: 3.2s
Throughput: ~6000 msg/s

---

# Step 3: Run Bad Threaded Version

python thread_bad_shared.py

Expected:
Sometimes errors such as:
StreamLostError
FrameUnderflow
connection closed unexpectedly

Or unstable throughput.

This demonstrates Pika channel is NOT thread safe.

---

# Step 4: Run Fixed Version

python thread_lock_fixed.py

Example output:

THREAD LOCK FIX RESULT
Messages: 25000
Time: 5.1s
Throughput: ~4800 msg/s

Stable execution.

---

# Step 5: Drain Queue Between Runs

python drain_queue.py

---

# Explanation

Shared channel across threads -> unsafe.

Lock ensures one thread publishes at a time.

Lock fixes race condition but reduces concurrency advantage.

---

Run async producer alone:

python async_producer.py

Run all benchmarks:

python benchmark_runner.py

Output:
benchmark_results.csv

Generate graph:

python plot_results.py

Output:
benchmark_graph.png
