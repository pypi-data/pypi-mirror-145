"""
This module contains  class for prodicing messages.
"""
from unittest import result
import grpc
from dpc.base.producer import ProduceBase
from dpc.protos.kafkapixy_pb2 import ProdRs, ProdRq
from dpc.protos.kafkapixy_pb2_grpc import KafkaPixyStub
from dpc.tools import utils
import logging


class Producer(ProduceBase):
    """Producer class"""

    def __init__(
        self,
        topic: str,
        message: bytes,
        address: str,
        port: str,
        # key_value: bytes,
        key_undefined=True,
    ):
        self.topic = topic
        self.message = message
        self.address = address
        self.port = port
        self.key_undefined = key_undefined
        # self.key_value = key_value
        self.client = utils.create_client(self.address, self.port)
        logging.getLogger().setLevel(logging.INFO)

    def produce(self) -> ProdRs:
        """Function for producing
        Args:
            topic (str): Name of the topic in the cluster to produce to.

            message: (ByteString): The message body

            _create_client:Produce pixy_client to produce

        Returns:
            response:  offset(str) and partition (str)
        """
        request = ProdRq(
            topic=self.topic,
            message=self.message,
            # key_value=self.key_value,
            # key_undefined=self.key_undefined,
        )
        client = utils.create_client(self.address, self.port)
        try:
            response = client.Produce(request, timeout=100)
            results = {"Partition": response.partition, "Offset": response.offset}
            logging.info(str(results))
            return result

        # Erro handling
        except grpc.RpcError as err:
            if hasattr(err, "code"):
                # HTTP Mapping: 499 Client Closed Request
                if err.code() == grpc.StatusCode.CANCELLED:
                    return err.details()
                # HTTP Mapping: 500 Internal Server Error
                if err.code() == grpc.StatusCode.UNKNOWN:
                    return err.details()
                # HTTP Mapping: 400 Bad Request
                if err.code() == grpc.StatusCode.INVALID_ARGUMENT:
                    return err.details()
                # HTTP Mapping: 504 Gateway Timeout
                if err.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                    return err.details()
                # HTTP Mapping: 404 Not Found.
                if err.code() == grpc.StatusCode.NOT_FOUND:
                    return err.details()
                # HTTP Mapping: 409 Conflict
                if err.code() == grpc.StatusCode.ALREADY_EXISTS:
                    return err.details()
                # HTTP Mapping: 403 Forbidden
                if err.code() == grpc.StatusCode.PERMISSION_DENIED:
                    return err.details()
                # HTTP Mapping: 401 Unauthorized
                if err.code() == grpc.StatusCode.UNAUTHENTICATED:
                    return err.details()
                # HTTP Mapping: 429 Too Many Requests
                if err.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:
                    return err.details()
                # HTTP Mapping: 400 Bad Request
                if err.code() == grpc.StatusCode.FAILED_PRECONDITION:
                    return err.details()
                # HTTP Mapping: 409 Conflict
                if err.code() == grpc.StatusCode.ABORTED:
                    return err.details()
                # HTTP Mapping: 400 Bad Request
                if err.code() == grpc.StatusCode.OUT_OF_RANGE:
                    return err.details()
                # HTTP Mapping: 501 Not Implemented
                if err.code() == grpc.StatusCode.UNIMPLEMENTED:
                    return err.details()
                # HTTP Mapping: 500 Internal Server Error
                if err.code() == grpc.StatusCode.INTERNAL:
                    return err.details()
                # HTTP Mapping: 503 Service Unavailable
                if err.code() == grpc.StatusCode.UNAVAILABLE:
                    return err.details()
                # HTTP Mapping: 500 Internal Server Error
                if err.code() == grpc.StatusCode.DATA_LOSS:
                    return err.details()
