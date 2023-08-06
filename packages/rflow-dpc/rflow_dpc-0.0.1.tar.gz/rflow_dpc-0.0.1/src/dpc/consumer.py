"""
This module contains  class for consuming messages.
"""
# from tkinter.messagebox import YES
from time import time
from tokenize import group
from unittest import result
import grpc
from dpc.base.consumer import ConsumeBase
from dpc.protos.kafkapixy_pb2 import ConsNAckRq, AckRq
from dpc.protos.kafkapixy_pb2_grpc import KafkaPixyStub
from dpc.tools import utils
import logging


class Consumer(ConsumeBase):
    """Consumer class"""

    def __init__(self, group: str, topic: str, address: str, port: str):
        self.group = group
        self.topic = topic
        self.address = address
        self.port = port
        self.client = utils.create_client(self.address, self.port)
        logging.getLogger().setLevel(logging.INFO)

    def consume(self) -> ConsNAckRq:
        """Function for consuming
        Args:
            topic (str): Name of the topic in the cluster to produce to.
            group (str): Name of a consumer group.
            _create_client:Produce pixy_client to consume
        Returns:
            response: offset(str) and message(Bytes) and key_undefined(bool)
        """
        ack_partition = None
        ack_offset = None
        request = ConsNAckRq(topic=self.topic, group=self.group)
        client = utils.create_client(self.address, self.port)
        keep_running = True
        timeout = 1000
        while keep_running:
            logging.info("Start sreaching data")
            if ack_offset is None:
                request.no_ack = True
                request.ack_partition = 0
                request.ack_offset = 0
                # logging.info("Set partition and offset to 0")
            else:
                request.no_ack = False
                request.ack_partition = ack_partition
                request.ack_offset = ack_offset
                # logging.info("Search partition and offset")
            try:
                response = client.ConsumeNAck(request, timeout=timeout)
                logging.info("connecting")
            except grpc.RpcError as err:
                if err.code() == grpc.StatusCode.NOT_FOUND:
                    ack_offset = None
                    logging.error(err.details())
                    continue
                else:
                    logging.error(err.details())
                    continue
            try:
                ack_partition = response.partition
                ack_offset = response.offset
                results = {
                    "Message": response.message,
                    "Partition": response.partition,
                    "Offset": response.offset,
                    "key": response.key_value,
                    "key_undefined": response.key_undefined,
                    "RecordHeader": response.headers,
                }
                logging.info("↓↓↓↓Got data from produce ↓↓↓↓")
                yield results
            except:
                logging.info("Reset")
                ack_offset = None


