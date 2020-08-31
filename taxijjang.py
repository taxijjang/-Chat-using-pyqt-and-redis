import redis
import time
taxijjang_r = redis.Redis(host='3.34.134.147', port=6379, db=0)
taxijjang_p = taxijjang_r.pubsub()
taxijjang_p.subscribe('chat_server')


cnt = 0
while True:
    cnt+= 1
    print(f"{cnt} .. Waiting For redisStarter...")

    message = taxijjang_p.get_message()

    if message:
        # Get data from message
        command = message['data']

        print(command)


    time.sleep(0.7)
