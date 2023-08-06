"""
This module contains abstract base class for producing messages.
"""
from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import List, ByteString, Dict
from dpc.protos.kafkapixy_pb2 import ProdRs


class ProduceBase(metaclass=ABCMeta):
    """Produce abstract base class"""

    def __init__(
        self,
        cluster: str,
        topic: str,
        message: bytes,
        address: str,
        port: str,
        headers: Dict,
        key_value: List,
        key_undefined: bool,
        async_mode: bool,
    ):
        """
        Initialize the produce args
        Args:
            cluster (str): Name of the kafka cluster to operate on

            topic (str): Name of the topic in the cluster to produce to.

            key_value (List,optional): Hash pf the key used to determine the partition to produce to

            key_undefined (bool): A boolean value to specify where the message is written to
            if provided  the messages are written in a random partition otherwise the hash
            of the key value  is used to determine the partition

            message: (ByteString): The message body

            async_mode: (bool): If true then the method returns immediately after Kafka-Pixy gets the
            produce request, and the message is written to Kafka asynchronously.
            In that case partition and offset returned in response should be ignored.
            If false, then a response is returned in accordance with the
            producer.required_acks parameter, that can be one of:
              * no_response:    the response is returned as soon as a produce request
                                is delivered to a partition leader Kafka broker.
              * wait_for_local: the response is returned as soon as data is written
                                to the disk by a partition leader Kafka broker.
              * wait_for_all:   the response is returned after all in-sync replicas
                                have data committed to disk.

            headers: (Dict) Headers to include with the published message

            address (str): Name of address number.

            port (str):Name of port number.
        """

        pass

    @abstractmethod
    def produce(self):
        """Produce abstract method"""
        pass
