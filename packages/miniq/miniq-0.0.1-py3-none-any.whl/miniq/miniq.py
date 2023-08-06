import grpc

from miniq.protobuf import queue_pb2 as pb2
from miniq.protobuf import queue_pb2_grpc as pb2_grpc


class MiniQ:
    """
    MiniQ client
    """

    _channel: grpc.Channel
    _stub: pb2_grpc.MiniQStub

    def __init__(self, address: str) -> None:
        # instantiate channel
        self._channel = grpc.insecure_channel(address)
        self._stub = pb2_grpc.MiniQStub(self._channel)

    def add_task(self, channel: str, data: bytes) -> None:
        """
        Add task to queue
        """
        req = pb2.AddTaskRequest(channel=channel, data=data)
        self._stub.AddTask(req)
