import pika

def inicializar_core():

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='Core', exchange_type='direct')

    result = channel.queue_declare(queue='Core', exclusive=False,durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='Core', queue=queue_name, routing_key=queue_name)

def consume_core(connection):
    channel = connection.channel

    # Definir la función que se ejecutará cuando se reciba un mensaje
    def callback(ch, method, properties, body):
        print(f" [x] Recibido: {body.decode()}")

        #TODO ASEGURAR QUE CORE EL REENVIE LOS MENSAJES A LAS COLAS ESPECIFICAS
        #Hacer en el callback, lectura del body y reenviar a la cola segun header destino...

    # Decirle a RabbitMQ que queremos recibir mensajes de 'Core'
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)


    channel.start_consuming()
