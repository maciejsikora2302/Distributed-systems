import pika, sys, os
from commons import *
from random import randint

#Getting random name
supplier_name = NAMES[randint(0,len(NAMES))].strip(' ')

#Handling message and order from client
def handle_delivery(channel, method, header, body):
    global supplier_name
    print(f"{supplier_name} | Processing order from {body.decode('utf-8')} for {method.routing_key}... Done. Sending delivery... ", end='')
    channel.basic_publish(exchange=SUPPLIER_EXCHNAGE, routing_key=f"{method.routing_key}.{body.decode('utf-8')}", body=bytes(supplier_name, encoding='utf-8'))
    print("Done, delivery sent.")

#Handling message from admin
def handle_admin_msg(channel, method, header, body):
    global supplier_name
    print(f"{supplier_name} | I have received msg from ADMIN: {body.decode('utf-8')}")

#Connecting to channel
parameters = pika.ConnectionParameters()
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

standard_setup(channel)

#Queue for message from admin
QNAME=f"supplier-{supplier_name}"
channel.queue_declare(QNAME)
channel.queue_bind(exchange=ADMIN_SUPPLIER_EXCHANGE, queue=QNAME)
channel.basic_consume(QNAME, handle_admin_msg, auto_ack=True)

#Listen for orders for those selected products
for item in sys.argv[1:]:
    channel.basic_consume(item, handle_delivery, auto_ack=True)

print("Awaiting for orders and messagess...")
channel.start_consuming()