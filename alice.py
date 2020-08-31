import redis
import socket

alice_r = redis.Redis(host='3.34.134.147', port=6379, db=0)

input_message = input()
user_ip = socket.gethostbyname(socket.getfqdn())

message = str(user_ip + " : " + input_message)
print(message)

alice_r.pubsub()
alice_r.publish('chat_server', message)