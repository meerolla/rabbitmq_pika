import pika
import threading
import time

QUEUE = "benchmark_queue"
THREADS = 10
MESSAGES_PER_THREAD = 2000

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()


lock = threading.Lock()

def worker(tid):

    for i in range(MESSAGES_PER_THREAD):

        with lock:

            channel.basic_publish(
                exchange="",
                routing_key=QUEUE,
                body=f"t{tid}-{i}"
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

    print("Finished in", end - start)

    connection.close()


if __name__ == "__main__":
    main()