"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import grpc

from .remote_pb2 import *
class RemoteExecutorStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    CreateTask:grpc.UnaryUnaryMultiCallable[
        global___CreateTaskRequest,
        global___CreateTaskResponse] = ...

    CancelTask:grpc.UnaryUnaryMultiCallable[
        global___CancelTaskRequest,
        global___CancelTaskResponse] = ...

    PostResult:grpc.UnaryUnaryMultiCallable[
        global___PostResultRequest,
        global___PostResultResponse] = ...

    WaitForResult:grpc.UnaryUnaryMultiCallable[
        global___WaitForResultRequest,
        global___WaitForResultResponse] = ...

    GetTask:grpc.UnaryUnaryMultiCallable[
        global___GetTaskRequest,
        global___GetTaskResponse] = ...

    RegisterApp:grpc.UnaryUnaryMultiCallable[
        global___RegisterAppRequest,
        global___RegisterAppResponse] = ...

    # Golang prototype
    RemoteCall:grpc.UnaryUnaryMultiCallable[
        global___RemoteCallRequest,
        global___RemoteCallResponse] = ...


class RemoteExecutorServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def CreateTask(self,
        request: global___CreateTaskRequest,
        context: grpc.ServicerContext,
    ) -> global___CreateTaskResponse: ...

    @abc.abstractmethod
    def CancelTask(self,
        request: global___CancelTaskRequest,
        context: grpc.ServicerContext,
    ) -> global___CancelTaskResponse: ...

    @abc.abstractmethod
    def PostResult(self,
        request: global___PostResultRequest,
        context: grpc.ServicerContext,
    ) -> global___PostResultResponse: ...

    @abc.abstractmethod
    def WaitForResult(self,
        request: global___WaitForResultRequest,
        context: grpc.ServicerContext,
    ) -> global___WaitForResultResponse: ...

    @abc.abstractmethod
    def GetTask(self,
        request: global___GetTaskRequest,
        context: grpc.ServicerContext,
    ) -> global___GetTaskResponse: ...

    @abc.abstractmethod
    def RegisterApp(self,
        request: global___RegisterAppRequest,
        context: grpc.ServicerContext,
    ) -> global___RegisterAppResponse: ...

    # Golang prototype
    @abc.abstractmethod
    def RemoteCall(self,
        request: global___RemoteCallRequest,
        context: grpc.ServicerContext,
    ) -> global___RemoteCallResponse: ...


def add_RemoteExecutorServicer_to_server(servicer: RemoteExecutorServicer, server: grpc.Server) -> None: ...
