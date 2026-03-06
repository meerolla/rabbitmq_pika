
from common import create_connection, QUEUE_NAME

def main():
    connection = create_connection()
    channel = connection.channel()

    count = 0

    while True:
        method, props, body = channel.basic_get(queue=QUEUE_NAME, auto_ack=True)
        if method is None:
            break
        count += 1

    connection.close()
    print(f"Drained {count} messages")

if __name__ == "__main__":
    main()
