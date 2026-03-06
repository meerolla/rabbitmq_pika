
import time
from common import create_connection, QUEUE_NAME

TOTAL_MESSAGES = 20000

def main():
    connection = create_connection()
    channel = connection.channel()

    start = time.time()

    for i in range(TOTAL_MESSAGES):
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=f"msg-{i}"
        )

    end = time.time()

    connection.close()

    duration = end - start
    print("\nSYNC RESULT")
    print(f"Messages: {TOTAL_MESSAGES}")
    print(f"Time: {duration:.2f}s")
    print(f"Throughput: {TOTAL_MESSAGES/duration:.2f} msg/s")

if __name__ == "__main__":
    main()
