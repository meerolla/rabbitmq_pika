import subprocess
import csv
import re

tests = [
    ("sync", "sync_producer.py"),
    ("thread_bad", "thread_bad_shared.py"),
    ("thread_lock", "thread_lock_fixed.py"),
    ("async", "async_producer.py"),
]

results = []

def run_test(name, script):

    print(f"\nRunning {name} test")

    result = subprocess.run(
        ["python", script],
        capture_output=True,
        text=True
    )

    output = result.stdout
    print(output)

    messages = re.search(r"Messages: (\d+)", output)
    time_val = re.search(r"Time: ([0-9.]+)", output)
    throughput = re.search(r"Throughput: ([0-9.]+)", output)

    if messages and time_val and throughput:
        results.append([
            name,
            int(messages.group(1)),
            float(time_val.group(1)),
            float(throughput.group(1))
        ])
    else:
        print("Could not parse output")


for name, script in tests:
    run_test(name, script)


with open("benchmark_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["test", "messages", "duration_sec", "throughput_msg_sec"])
    writer.writerows(results)


print("\nResults saved to benchmark_results.csv")