import pika
from commons import *

#Handling consumes from lients and spulliers

def consume_client(channel, method, properties, body):
    print(f"LOG-CLIENT: Client {body.decode('utf-8')} has send a request for {method.routing_key}")

def consume_supplier(channel, method, properties, body):
    print(f"LOG-SUPPLIER: Supplier {body.decode('utf-8')} has send a confirmation for {method.routing_key.split('.')[0]} for client {method.routing_key.split('.')[1]}")

#Connect to channel
parameters = pika.ConnectionParameters()
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

#Standard setup (in commons.py)
standard_setup(channel)

#Publishing hello message from Admin to all end-users on the communication
print(f'LOG-ADMIN: Sending \'ADMIN HELLO MESSAGE FOR CLIENT\' to clients')
channel.basic_publish(exchange=ADMIN_CLIENT_EXCHANGE, body=bytes("ADMIN HELLO MESSAGE FOR CLIENT", encoding='UTF-8'), routing_key='ADMIN.A')
print(f'LOG-ADMIN: Sending \'ADMIN HELLO MESSAGE FOR SUPPLIER\' to suppliers')
channel.basic_publish(exchange=ADMIN_SUPPLIER_EXCHANGE, body=bytes("ADMIN HELLO MESSAGE FOR SUPPLIER", encoding='UTF-8'), routing_key='')

#Sending message in three variants

#All clients
print(f'LOG-ADMIN: Sending \'Good luck on your journey! Remember to prioritise your safety first!\' to clients')
channel.basic_publish(exchange=ADMIN_CLIENT_EXCHANGE, body=bytes('Good luck on your journey! Remember to prioritise your safety first!', encoding='utf-8'), routing_key='ADMIN.A')

#All suppliers
print(f'LOG-ADMIN: Sending \'Keep up the good work!\' to suppliers')
channel.basic_publish(exchange=ADMIN_SUPPLIER_EXCHANGE, body=bytes('Keep up the good work!', encoding='utf-8'), routing_key='')

#All clients and suppliers
print('LOG-ADMIN: Sending \'Did you know that distributed systems are the best subject on WIEiT?\' to everyone')
channel.basic_publish(exchange=ADMIN_CLIENT_EXCHANGE, body=bytes('Did you know that distributed systems are the best subject on WIEiT?', encoding='utf-8'), routing_key='ADMIN.A')
channel.basic_publish(exchange=ADMIN_SUPPLIER_EXCHANGE, body=bytes('Did you know that distributed systems are the best subject on WIEiT?', encoding='utf-8'), routing_key='')


#Starting consuming messages for log purposes
channel.basic_consume("admin-order", consume_client, auto_ack=True)
channel.basic_consume("admin-delivery", consume_supplier, auto_ack=True)
channel.start_consuming()