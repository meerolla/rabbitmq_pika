
import asyncio
import time
import aio_pika

QUEUE_NAME = "benchmark_queue"
TOTAL_MESSAGES = 20000

async def run():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()

    start = time.time()

    # Below is publish->wait, publish->wait ...
    # for i in range(TOTAL_MESSAGES):
    #     await channel.default_exchange.publish(
    #         aio_pika.Message(body=f"msg-{i}".encode()),
    #         routing_key=QUEUE_NAME
    #     )

    # Below is publish, publish...... and wait
    tasks = []

    for i in range(TOTAL_MESSAGES):
        tasks.append(
            channel.default_exchange.publish(
                aio_pika.Message(body=f"msg-{i}".encode()),
                routing_key=QUEUE_NAME
            )
        )

    await asyncio.gather(*tasks)

    end = time.time()
    await connection.close()

    duration = end - start
    rate = TOTAL_MESSAGES / duration

    print("\nASYNC RESULT")
    print(f"Messages: {TOTAL_MESSAGES}")
    print(f"Time: {duration:.2f}s")
    print(f"Throughput: {rate:.2f} msg/s")

    return TOTAL_MESSAGES, duration, rate


if __name__ == "__main__":
    asyncio.run(run())
