
import threading
import time
from common import create_connection, QUEUE_NAME

THREADS = 5
MESSAGES_PER_THREAD = 5000

connection = create_connection()
channel = connection.channel()

lock = threading.Lock()

def worker(tid):
    for i in range(MESSAGES_PER_THREAD):
        with lock:
            channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=f"thread-{tid}-{i}"
            )

def main():
    threads = []
    start = time.time()

    for i in range(THREADS):
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end = time.time()
    connection.close()

    total = THREADS * MESSAGES_PER_THREAD

    print("\nTHREAD LOCK FIX RESULT")
    print(f"Messages: {total}")
    print(f"Time: {end-start:.2f}s")
    print(f"Throughput: {total/(end-start):.2f} msg/s")

if __name__ == "__main__":
    main()
