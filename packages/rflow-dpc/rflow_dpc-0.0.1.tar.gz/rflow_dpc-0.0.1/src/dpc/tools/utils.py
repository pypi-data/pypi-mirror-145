import grpc
from dpc.protos.kafkapixy_pb2_grpc import KafkaPixyStub


def create_client(address: str, port: str, secure=False):
    """Function for creating client
    Args:
        address (str): Name of address number.
        port (str):Name of port number.
        secure(bool): boolean value to specify the channel is secure or not.Default is set to False.
    Returns:
        The pixy_client
    """
    ip_address_key = address + ":" + port
    if secure:
        pass
    else:
        grpc_channel = grpc.insecure_channel(ip_address_key)
        pixy_client = KafkaPixyStub(grpc_channel)
        return pixy_client
