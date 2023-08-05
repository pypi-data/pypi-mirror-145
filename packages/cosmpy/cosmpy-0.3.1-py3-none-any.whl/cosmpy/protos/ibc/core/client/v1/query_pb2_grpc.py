# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from ibc.core.client.v1 import query_pb2 as ibc_dot_core_dot_client_dot_v1_dot_query__pb2


class QueryStub(object):
    """Query provides defines the gRPC querier service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ClientState = channel.unary_unary(
                '/ibc.core.client.v1.Query/ClientState',
                request_serializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientStateRequest.SerializeToString,
                response_deserializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientStateResponse.FromString,
                )
        self.ClientStates = channel.unary_unary(
                '/ibc.core.client.v1.Query/ClientStates',
                request_serializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientStatesRequest.SerializeToString,
                response_deserializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientStatesResponse.FromString,
                )
        self.ConsensusState = channel.unary_unary(
                '/ibc.core.client.v1.Query/ConsensusState',
                request_serializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryConsensusStateRequest.SerializeToString,
                response_deserializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryConsensusStateResponse.FromString,
                )
        self.ConsensusStates = channel.unary_unary(
                '/ibc.core.client.v1.Query/ConsensusStates',
                request_serializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryConsensusStatesRequest.SerializeToString,
                response_deserializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryConsensusStatesResponse.FromString,
                )
        self.ClientParams = channel.unary_unary(
                '/ibc.core.client.v1.Query/ClientParams',
                request_serializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientParamsRequest.SerializeToString,
                response_deserializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientParamsResponse.FromString,
                )


class QueryServicer(object):
    """Query provides defines the gRPC querier service
    """

    def ClientState(self, request, context):
        """ClientState queries an IBC light client.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClientStates(self, request, context):
        """ClientStates queries all the IBC light clients of a chain.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConsensusState(self, request, context):
        """ConsensusState queries a consensus state associated with a client state at
        a given height.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConsensusStates(self, request, context):
        """ConsensusStates queries all the consensus state associated with a given
        client.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClientParams(self, request, context):
        """ClientParams queries all parameters of the ibc client.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ClientState': grpc.unary_unary_rpc_method_handler(
                    servicer.ClientState,
                    request_deserializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientStateRequest.FromString,
                    response_serializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientStateResponse.SerializeToString,
            ),
            'ClientStates': grpc.unary_unary_rpc_method_handler(
                    servicer.ClientStates,
                    request_deserializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientStatesRequest.FromString,
                    response_serializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientStatesResponse.SerializeToString,
            ),
            'ConsensusState': grpc.unary_unary_rpc_method_handler(
                    servicer.ConsensusState,
                    request_deserializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryConsensusStateRequest.FromString,
                    response_serializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryConsensusStateResponse.SerializeToString,
            ),
            'ConsensusStates': grpc.unary_unary_rpc_method_handler(
                    servicer.ConsensusStates,
                    request_deserializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryConsensusStatesRequest.FromString,
                    response_serializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryConsensusStatesResponse.SerializeToString,
            ),
            'ClientParams': grpc.unary_unary_rpc_method_handler(
                    servicer.ClientParams,
                    request_deserializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientParamsRequest.FromString,
                    response_serializer=ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientParamsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ibc.core.client.v1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Query(object):
    """Query provides defines the gRPC querier service
    """

    @staticmethod
    def ClientState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ibc.core.client.v1.Query/ClientState',
            ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientStateRequest.SerializeToString,
            ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientStateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClientStates(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ibc.core.client.v1.Query/ClientStates',
            ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientStatesRequest.SerializeToString,
            ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientStatesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConsensusState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ibc.core.client.v1.Query/ConsensusState',
            ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryConsensusStateRequest.SerializeToString,
            ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryConsensusStateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConsensusStates(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ibc.core.client.v1.Query/ConsensusStates',
            ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryConsensusStatesRequest.SerializeToString,
            ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryConsensusStatesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClientParams(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ibc.core.client.v1.Query/ClientParams',
            ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientParamsRequest.SerializeToString,
            ibc_dot_core_dot_client_dot_v1_dot_query__pb2.QueryClientParamsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
