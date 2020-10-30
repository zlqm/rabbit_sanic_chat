import asyncio
import logging
import json
import uuid

import pika
import aio_pika

logger = logging.getLogger('sanic.root')

loop = asyncio.get_event_loop()


class MQClient:
    def __init__(self):
        self._connection_parameters = pika.ConnectionParameters(
            host='localhost')
        self._exchange = 'sanic'
        self._queue = 'sanic_' + str(uuid.uuid4())

    async def start(self):
        logger.info('connecting to rabbitmq')
        self._connection = await aio_pika.connect(
            'amqp://guest:guest@rabbitmq/')
        #self._connection_parameters)
        self._channel = await self._connection.channel()
        self._logs_exchange = await self._channel.declare_exchange(
            self._exchange,
            aio_pika.ExchangeType.FANOUT,
        )
        queue = await self._channel.declare_queue(self._queue, exclusive=True)
        await queue.bind(self._logs_exchange)
        await queue.consume(self.on_message)
        logger.info('rabbitmq init done')

    async def on_message(self, message):
        async with message.process():
            logger.info('receive message: %s', message.body)
            data = json.dumps({'message': message.body.decode()})
            await self.websocket.send(data)

    async def publish(self, msg):
        logger.info('publish %s', msg)
        message = aio_pika.Message(
            msg.encode(), delivery_mode=aio_pika.DeliveryMode.PERSISTENT)
        await self._logs_exchange.publish(message, routing_key='')
