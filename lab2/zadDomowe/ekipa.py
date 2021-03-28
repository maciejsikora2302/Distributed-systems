import pika, sys, os
from commons import *
from random import randint
from threading import Thread
from time import sleep

#Persing messages to differenciate between messages from admin and messages from suppliers
def callback(channel, method, properties, body):
    info = method.routing_key.split('.')[0]
    if info == "ADMIN":
        print(f"I ({team_name}) have received message from admin: {body.decode('utf-8')}")
    else:
        print(f"Received order compleation for {info} from {body.decode('utf-8')}")

#Opening connection
connection = pika.BlockingConnection(pika.ConnectionParameters())
channel = connection.channel()

#Getting random name
team_name = NAMES[randint(0,len(NAMES)-1)].replace(" ", '')

standard_setup(channel)

#Queue for client to receive messages from admin/supplier
QNAME = f'client-{team_name}'
channel.queue_declare(queue=QNAME)
channel.queue_bind(exchange=SUPPLIER_EXCHNAGE, queue=QNAME, routing_key=f'*.{team_name}')
channel.queue_bind(exchange=ADMIN_CLIENT_EXCHANGE, queue=QNAME) #Admin will post msg here

#Sending orders

# air = ['tlen' for _ in range(randint(0, 20))]
# boots = ['buty' for _ in range(randint(0, 10))]
# backpack = ['plecak' for _ in range(randint(0, 10))]

# orders_rand = air + boots + backpack
# orders = ['tlen', 'tlen', 'buty', 'plecak', 'buty']
print("Please inpurt orders seperated by spacebar and confirmed by enter:")
orders = input()
orders = orders.split(' ')
for o in orders:
    if o in ITEMS:
        print(f"{team_name} | Sending an order for {o}")
        channel.basic_publish(exchange=CLIENT_EXCHANGE, routing_key=o, body=bytes(team_name, encoding='utf-8'))


#Awaiting for delivery
channel.basic_consume(QNAME, callback, auto_ack=True)
channel.start_consuming()
