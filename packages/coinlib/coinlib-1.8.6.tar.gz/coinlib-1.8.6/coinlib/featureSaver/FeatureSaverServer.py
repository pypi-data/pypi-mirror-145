import asyncio
import threading

import aio_pika
from aio_pika import IncomingMessage
from chipmunkdb.ChipmunkDb import ChipmunkDb

import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import simplejson as json

import ipynb_path
from grpc._cython.cygrpc import CompressionAlgorithm
from grpc._cython.cygrpc import CompressionLevel
import grpc
import inspect
from coinlib.Registrar import Registrar

registrar = Registrar()

class FeatureSaverServer:


    def connect(self):
        self.channel = self.createChannel()
        #self.logicInterface = stats.FeatureSaverStub(self.channel)
        pass

    def createChannel(self):
        chan_ops = [('grpc.max_receive_message_length', 1000 * 1024 * 1024),
                    ('grpc.default_compression_algorithm', CompressionAlgorithm.gzip),
                    ('grpc.grpc.default_compression_level', CompressionLevel.high)]
        return grpc.insecure_channel(self.registrar.get_coinlib_backend_grpc(), options=chan_ops,
                                     compression=grpc.Compression.Gzip)

    async def latest_data_feature_received(self, message_data):

        chipmunk = ChipmunkDb("localhost")

        if "source" in message_data:
            data = message_data["data"]
            identifier = message_data["source"]

            keylist = []
            for key in data:
                val = data[key]
                id = val["identifier"]
                if "group" in val and val["group"] is not None and val["group"] != "":
                    id = val["group"]+"."+val["identifier"]
                keyentry = {
                    "key": id,
                    "value": val["value"]
                }
                tags = []
                if "symbol" in val and val["symbol"] is not None:
                    tags.append(val["symbol"])
                if "exchange" in val and val["exchange"] is not None:
                    tags.append(val["exchange"])
                if len(tags) > 0:
                    keyentry["tags"] = tags
                keylist.append(keyentry)

            chipmunk.save_keys_to_storage(identifier, keylist)

    def logger(self):
        return registrar.logger


    async def run_process(self):
        connection = await aio_pika.connect_robust(
            "amqp://thoren:thoren@78.47.96.243:5672/", loop=self.loop
        )

        async with connection:

            # Creating channel
            self.channel = await connection.channel()  # type: aio_pika.Channel
            await self.channel.set_qos(prefetch_count=1)

            # Declaring queue
            queue = await self.channel.declare_queue(
                "latest_feature_queue",
                durable=True
            )
            async with queue.iterator() as queue_iter:
                # Cancel consuming after __aexit__
                async for message in queue_iter:
                    async with message.process():
                        try:
                            message_data = json.loads(message.body)
                            await self.latest_data_feature_received(message_data)

                        except Exception as e:
                            self.logger().error(e)
                            pass


            print("ifnished")


        return True

    def start_Threaded(self):

        self.loop = asyncio.new_event_loop()

        self.loop.run_until_complete(self.run_process())

    def start(self):

        self.thread = threading.Thread(target=self.start_Threaded, args=[], daemon=True)
        self.thread.start()

        try:
            self.thread.join()
        except Exception as e:
            pass


