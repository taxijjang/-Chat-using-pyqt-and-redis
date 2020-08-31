import redis
import time
bob_r = redis.Redis(host='3.34.134.147', port=6379, db=0)
bob_p = bob_r.pubsub()
bob_p.subscribe('chat_server')


cnt = 0
while True:
    cnt+= 1
    print(f"{cnt} .. Waiting For redisStarter...")

    message = bob_p.get_message()

    if message:
        # Get data from message
        command = message['data']

        print(command)


    time.sleep(0.7)
