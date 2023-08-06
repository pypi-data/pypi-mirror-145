"""
This module contains abstract base class for consuming messages.
"""
from abc import ABCMeta, abstractmethod
from typing import List, ByteString, Dict
from dpc.protos.kafkapixy_pb2 import ConsNAckRq


class ConsumeBase(metaclass=ABCMeta):
    """Consume abstract base class"""

    def __init__(
        self,
        cluster_name: str,
        topic: str,
        group: str,
        no_ack: bool,
        auto_ack: bool,
        ack_partition: int,
        ack_offset: int,
        address: str,
        port: str,
    ):
        """Initialize the consume args
        Args:
            cluster_name (str): Name of the kafka cluster to operate on

            topic (str): Name of the topic in the cluster to produce to.

            group (str): Name of a consumer group.

            no_ack(bool): If true then no message is acknowledged by the request.

            auto_ack(book): If true and no_ack is false then the message returned by the requests is automatically acknowledged by Kafka-Pixy before the request completes.

            ack_partition(int32),ack_offset(int64):If both no_ack and auto_ack are false (by default), then ack_partition and ack_offset along with cluster-group-topic determine the message that should be acknowledged by the request.

            address (str): Name of address number.

            port (str):Name of port number.
        """
        pass

    @abstractmethod
    def consume(self):
        """Cousume abstract method"""
        pass
