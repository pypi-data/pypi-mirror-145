import asyncio
import threading
import random
import string
import aio_pika
import simplejson as json
from aio_pika import ExchangeType, Message, DeliveryMode

from coinlib import Registrar, helper
from coinlib.feature.FeatureDTO import RabbitInfo


class CollectionInterface:
    def __init__(self, name: str, cdn: str = None, loop = None):
        self.rabbit_info = RabbitInfo()
        self.registrar = Registrar()
        self.commandRegistry = []
        self.commandReceived = {}
        if not self.registrar.isLiveEnvironment():
            name = "dev_"+name
        self.name = name
        if cdn is None:
            cdn = "cdn1"
        self.cdn = cdn

        if loop is None:
            loop = asyncio.new_event_loop()
        self.loop = loop

        letters = string.ascii_lowercase + string.digits + string.ascii_uppercase
        self.session_id = ''.join(random.choice(letters) for i in range(28))


        _thread = threading.Thread(target=self.startMQWorkerThread, args=())
        _thread.start()

        # creating outgoings
        self.loop.run_until_complete(self.connect())
        self.loop.run_until_complete(self._generate_channels())

        pass

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            "amqp://" + self.rabbit_info.user + ":" + self.rabbit_info.pwd + "@" + self.rabbit_info.ip + ":" + self.rabbit_info.port + "/",
            loop=self.loop
            )

    def _send_command_saver_sync(self, command: str, params: object = None):
        com = self.loop.run_until_complete(self._send_command_saver(command, params))

        if com is None:
            return None

        async def _wait_for_command_answer():
            for x in range(5000):
                if com["transactionId"] in self.commandReceived:
                    answer = self.commandReceived[com["transactionId"]]
                    if answer:
                        del self.commandReceived[com["transactionId"]]
                        return answer
                await asyncio.sleep(0.001)

            return None

        future = self.loop.run_until_complete(_wait_for_command_answer())
        if future is not None:
            if future["success"] == False:
                raise Exception(future["error"])
            return future["data"]
        return None

    def _send_command_query_sync(self, command: str, params: object = None):
        com = self.loop.run_until_complete(self._send_command_query(command, params))

        if com is None:
            return None

        async def _wait_for_command_answer():
            for x in range(5000):
                if com["transactionId"] in self.commandReceived:
                    answer = self.commandReceived[com["transactionId"]]
                    if answer:
                        del self.commandReceived[com["transactionId"]]
                        return answer
                await asyncio.sleep(0.001)

            return None

        future = self.loop.run_until_complete(_wait_for_command_answer())
        if future is not None:
            if future["success"] == False:
                raise Exception(future["error"])
            return future["data"]
        return None

    async def _generate_channels(self):

        # Creating channel
        self.save_channel = await self.connection.channel()

        self.save_exchange = await self.save_channel.declare_exchange("data_collection_save_"+self.cdn, "topic",
                                                                auto_delete=False, durable=True)

        self.save_queue = await self.save_channel.declare_queue("data_collection_save_" + self.cdn,
                                                                auto_delete=False,
                                                                durable=True)

        await self.save_queue.bind(self.save_exchange, "command")

        # Declaring queue
        self.query_channel = await self.connection.channel()

        self.query_exchange = await self.query_channel.declare_exchange("data_collection_query_"+self.cdn, "topic",
                                                             auto_delete=False, durable=True)

        self.query_queue = await self.query_channel.declare_queue("data_collection_query_" + self.cdn,
                                                                  auto_delete=False,
                                                                  durable=True)

        await self.query_queue.bind(self.query_exchange, "command")



    async def _send_command_saver(self, command: str, params: object = None):
        try:
            letters = string.ascii_lowercase + string.digits + string.ascii_uppercase
            transactionid = ''.join(random.choice(letters) for i in range(28))
            try:

                message_raw = {
                    "transactionId": transactionid,
                    "routing_key": self.registrar.environment + "_" + self.session_id,
                    "command": command,
                    "params": params
                }
                self.commandRegistry.append(message_raw)

                message_body = json.dumps(message_raw, default=helper.serializeDTO)

                message = Message(
                    str.encode(message_body),
                    delivery_mode=DeliveryMode.PERSISTENT
                )

                await self.save_exchange.publish(
                    message,
                    "command",
                )

                return message_raw

            except Exception as e:
                print(e)
                pass
        except Exception as e:
            print(e)
        return None

    async def _send_command_query(self, command: str, params: object = None):
        try:
            letters = string.ascii_lowercase + string.digits + string.ascii_uppercase
            transactionid = ''.join(random.choice(letters) for i in range(28))
            try:
                message_raw = {
                    "transactionId": transactionid,
                    "routing_key": self.registrar.environment + "_" + self.session_id,
                    "command": command,
                    "params": params
                }
                self.commandRegistry.append(message_raw)

                message_body = json.dumps(message_raw, default=helper.serializeDTO)

                message = Message(
                    str.encode(message_body),
                    delivery_mode=DeliveryMode.PERSISTENT
                )

                # Sending the message

                await self.query_exchange.publish(
                    message,
                    "command",
                )

                return message_raw

            except Exception as e:
                    pass
        except Exception as e:
            print(e)
        return None

    def startMQWorkerThread(self):
        self.listener_loop = asyncio.new_event_loop()
        self.listener_loop.run_until_complete(self.startMQWorker())

    async def startMQWorker(self):

        queue_name = "data_collection_response_"+self.cdn
        connection = await aio_pika.connect_robust(
            "amqp://" + self.rabbit_info.user + ":" + self.rabbit_info.pwd + "@" + self.rabbit_info.ip + ":" + self.rabbit_info.port + "/",
            loop=self.listener_loop
            )

        # Creating channel
        self.channel = await connection.channel()  # type: aio_pika.Channel

        # Declaring queue
        await self.channel.declare_exchange(
            queue_name.lower(),
            ExchangeType.TOPIC,
            durable=True,
        )

        # Declaring queue
        exchange = await self.channel.get_exchange(
            queue_name
        )
        routing_key = self.registrar.environment + "_" + self.session_id
        queue = await self.channel.declare_queue(auto_delete=True)
        await queue.bind(exchange, routing_key=routing_key.lower())
        async with queue.iterator() as queue_iter:
            try:
                # Cancel consuming after __aexit__
                async for message in queue_iter:
                    async with message.process():
                        try:
                            message_raw = json.loads(message.body)
                            self._on_command_receive(message_raw)
                        except Exception as e:
                            self.logger().error(e)
                            pass
            except Exception as e:
                print(e)
                pass
        return True

    def logger(self):
        return self.registrar.logger

    def _on_command_receive(self, message):
        command = next((x for x in self.commandRegistry if x["transactionId"] == message["transactionId"]), None)
        if command is not None:
            self.commandRegistry = [x for x in self.commandRegistry if x["transactionId"] != message["transactionId"]]
            self.commandReceived[command["transactionId"]] = message


    def query(self, query):
        data = self._send_command_query_sync("query", {"collection": self.name, "query": query})
        return data

    def len(self):
        result = self._send_command_saver_sync("count", {"collection": self.name})
        return result

    def delete(self, query: object):
        result = self._send_command_saver_sync("delete", {"collection": self.name, "query": query})
        return result

    def update(self, query: object, data: object):
        result = self._send_command_saver_sync("update", {"collection": self.name, "query": query, "data": data})
        return result

    def insert(self, data: [object]):
        result = self._send_command_saver_sync("insert", {"collection": self.name, "data": data})
        return result

    def insertOrUpdate(self, query: object, data: object):
        result = self._send_command_saver_sync("insertOrUpdate", {"collection": self.name, "query": query, "data": data})
        return result
