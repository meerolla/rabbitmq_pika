
# RabbitMQ Producer Benchmark Lab 🚀

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.x-orange)
![Docker](https://img.shields.io/badge/Docker-required-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A hands‑on lab to explore **RabbitMQ producer performance and Pika thread‑safety** using Python.

This project compares different publishing models:

- **Sync Producer** – baseline RabbitMQ publishing
- **Threaded Producer (unsafe)** – demonstrates Pika thread‑safety issues
- **Thread‑safe Producer** – fix using `threading.Lock`
- **Async Producer** – asynchronous publishing using `aio-pika`
- **Benchmark Runner** – automated performance comparison
- **Visualization** – throughput graph generation

---

# Architecture

```
Producer Models
     │
     ▼
 RabbitMQ Queue
     │
     ▼
Benchmark Runner
     │
     ▼
CSV Results
     │
     ▼
Graph Visualization
```

---

# Project Structure

```
rabbitmq_pika_thread_demo
│
├── setup_queue.py
├── sync_producer.py
├── thread_bad_shared.py
├── thread_lock_fixed.py
├── async_producer.py
├── drain_queue.py
│
├── benchmark_runner.py
├── plot_results.py
│
└── README.md
```

---

# Prerequisites

Create virtual environment

```bash
python -m venv .env
source .env/bin/activate
```

Install dependencies

```bash
pip install pika aio-pika matplotlib
```

---

# Start RabbitMQ

```bash
docker run -d   --name rabbit   -p 5672:5672   -p 15672:15672   rabbitmq:3-management
```

RabbitMQ Management UI:

```
http://localhost:15672
username: guest
password: guest
```

---

# Step 1 — Create Queue

```bash
python setup_queue.py
```

---

# Step 2 — Run Sync Producer

```bash
python sync_producer.py
```

Example result

```
SYNC RESULT
Messages: 20000
Time: 1.33s
Throughput: ~15000 msg/sec
```

---

# Step 3 — Demonstrate Thread Safety Issue

```bash
python thread_bad_shared.py
```

Expected behavior:

Possible errors such as:

```
StreamLostError
FrameUnderflow
ConnectionClosed
```

This demonstrates:

> **Pika channels are NOT thread‑safe**.

---

# Step 4 — Thread‑Safe Version

```bash
python thread_lock_fixed.py
```

Uses

```
threading.Lock()
```

to serialize access to the channel.

---

# Step 5 — Drain Queue

```bash
python drain_queue.py
```

Removes messages between runs to keep benchmarks consistent.

---

# Step 6 — Async Producer

```bash
python async_producer.py
```

Uses **aio‑pika** for asynchronous RabbitMQ publishing.

---

# Run Full Benchmark

```bash
python benchmark_runner.py
```

Output file

```
benchmark_results.csv
```

Example:

```
test,messages,duration_sec,throughput_msg_sec
sync,20000,1.33,15064.87
thread_lock,25000,2.41,10392.78
async,20000,8.80,2273.16
```

---

# Generate Throughput Graph

```bash
python plot_results.py
```

Creates:

```
benchmark_graph.png
```

Example comparison

| Producer | Throughput |
|--------|-------------|
| Sync | ~15000 msg/s |
| Thread + Lock | ~10300 msg/s |
| Async | ~2200 msg/s |

---

# Key Takeaways

- **Pika channels are not thread‑safe**
- Shared channel across threads can corrupt connections
- Lock fixes race conditions but reduces concurrency
- Async helps when many operations run concurrently

---

# Learning Goals

This lab demonstrates:

- RabbitMQ producer performance patterns
- Pika thread‑safety limitations
- Sync vs Thread vs Async publishing
- Simple benchmarking methodology

---