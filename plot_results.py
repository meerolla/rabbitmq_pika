
import csv
import matplotlib.pyplot as plt

tests = []
throughputs = []

with open("benchmark_results.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        tests.append(row["test"])
        throughputs.append(float(row["throughput_msg_sec"]))

plt.bar(tests, throughputs)
plt.xlabel("Test Type")
plt.ylabel("Throughput (msg/sec)")
plt.title("RabbitMQ Producer Benchmark Comparison")
plt.savefig("benchmark_graph.png")
plt.show()
