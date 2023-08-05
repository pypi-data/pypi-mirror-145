# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmwasm/wasm/v1/query.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from cosmwasm.wasm.v1 import types_pb2 as cosmwasm_dot_wasm_dot_v1_dot_types__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1c\x63osmwasm/wasm/v1/query.proto\x12\x10\x63osmwasm.wasm.v1\x1a\x14gogoproto/gogo.proto\x1a\x1c\x63osmwasm/wasm/v1/types.proto\x1a\x1cgoogle/api/annotations.proto\x1a*cosmos/base/query/v1beta1/pagination.proto\"+\n\x18QueryContractInfoRequest\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\"w\n\x19QueryContractInfoResponse\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x43\n\rcontract_info\x18\x02 \x01(\x0b\x32\x1e.cosmwasm.wasm.v1.ContractInfoB\x0c\xd0\xde\x1f\x01\xc8\xde\x1f\x00\xea\xde\x1f\x00:\x04\xe8\xa0\x1f\x01\"j\n\x1bQueryContractHistoryRequest\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12:\n\npagination\x18\x02 \x01(\x0b\x32&.cosmos.base.query.v1beta1.PageRequest\"\x9e\x01\n\x1cQueryContractHistoryResponse\x12\x41\n\x07\x65ntries\x18\x01 \x03(\x0b\x32*.cosmwasm.wasm.v1.ContractCodeHistoryEntryB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b\x32\'.cosmos.base.query.v1beta1.PageResponse\"j\n\x1bQueryContractsByCodeRequest\x12\x0f\n\x07\x63ode_id\x18\x01 \x01(\x04\x12:\n\npagination\x18\x02 \x01(\x0b\x32&.cosmos.base.query.v1beta1.PageRequest\"n\n\x1cQueryContractsByCodeResponse\x12\x11\n\tcontracts\x18\x01 \x03(\t\x12;\n\npagination\x18\x02 \x01(\x0b\x32\'.cosmos.base.query.v1beta1.PageResponse\"k\n\x1cQueryAllContractStateRequest\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12:\n\npagination\x18\x02 \x01(\x0b\x32&.cosmos.base.query.v1beta1.PageRequest\"\x8b\x01\n\x1dQueryAllContractStateResponse\x12-\n\x06models\x18\x01 \x03(\x0b\x32\x17.cosmwasm.wasm.v1.ModelB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b\x32\'.cosmos.base.query.v1beta1.PageResponse\"C\n\x1cQueryRawContractStateRequest\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x12\n\nquery_data\x18\x02 \x01(\x0c\"-\n\x1dQueryRawContractStateResponse\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\"]\n\x1eQuerySmartContractStateRequest\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12*\n\nquery_data\x18\x02 \x01(\x0c\x42\x16\xfa\xde\x1f\x12RawContractMessage\"G\n\x1fQuerySmartContractStateResponse\x12$\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x42\x16\xfa\xde\x1f\x12RawContractMessage\"#\n\x10QueryCodeRequest\x12\x0f\n\x07\x63ode_id\x18\x01 \x01(\x04\"\xa5\x01\n\x10\x43odeInfoResponse\x12!\n\x07\x63ode_id\x18\x01 \x01(\x04\x42\x10\xe2\xde\x1f\x06\x43odeID\xea\xde\x1f\x02id\x12\x0f\n\x07\x63reator\x18\x02 \x01(\t\x12K\n\tdata_hash\x18\x03 \x01(\x0c\x42\x38\xfa\xde\x1f\x34github.com/tendermint/tendermint/libs/bytes.HexBytes:\x04\xe8\xa0\x1f\x01J\x04\x08\x04\x10\x05J\x04\x08\x05\x10\x06\"r\n\x11QueryCodeResponse\x12?\n\tcode_info\x18\x01 \x01(\x0b\x32\".cosmwasm.wasm.v1.CodeInfoResponseB\x08\xd0\xde\x1f\x01\xea\xde\x1f\x00\x12\x16\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x42\x08\xea\xde\x1f\x04\x64\x61ta:\x04\xe8\xa0\x1f\x01\"O\n\x11QueryCodesRequest\x12:\n\npagination\x18\x01 \x01(\x0b\x32&.cosmos.base.query.v1beta1.PageRequest\"\x8f\x01\n\x12QueryCodesResponse\x12<\n\ncode_infos\x18\x01 \x03(\x0b\x32\".cosmwasm.wasm.v1.CodeInfoResponseB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b\x32\'.cosmos.base.query.v1beta1.PageResponse\"U\n\x17QueryPinnedCodesRequest\x12:\n\npagination\x18\x02 \x01(\x0b\x32&.cosmos.base.query.v1beta1.PageRequest\"z\n\x18QueryPinnedCodesResponse\x12!\n\x08\x63ode_ids\x18\x01 \x03(\x04\x42\x0f\xc8\xde\x1f\x00\xe2\xde\x1f\x07\x43odeIDs\x12;\n\npagination\x18\x02 \x01(\x0b\x32\'.cosmos.base.query.v1beta1.PageResponse2\xf7\n\n\x05Query\x12\x95\x01\n\x0c\x43ontractInfo\x12*.cosmwasm.wasm.v1.QueryContractInfoRequest\x1a+.cosmwasm.wasm.v1.QueryContractInfoResponse\",\x82\xd3\xe4\x93\x02&\x12$/cosmwasm/wasm/v1/contract/{address}\x12\xa6\x01\n\x0f\x43ontractHistory\x12-.cosmwasm.wasm.v1.QueryContractHistoryRequest\x1a..cosmwasm.wasm.v1.QueryContractHistoryResponse\"4\x82\xd3\xe4\x93\x02.\x12,/cosmwasm/wasm/v1/contract/{address}/history\x12\xa4\x01\n\x0f\x43ontractsByCode\x12-.cosmwasm.wasm.v1.QueryContractsByCodeRequest\x1a..cosmwasm.wasm.v1.QueryContractsByCodeResponse\"2\x82\xd3\xe4\x93\x02,\x12*/cosmwasm/wasm/v1/code/{code_id}/contracts\x12\xa7\x01\n\x10\x41llContractState\x12..cosmwasm.wasm.v1.QueryAllContractStateRequest\x1a/.cosmwasm.wasm.v1.QueryAllContractStateResponse\"2\x82\xd3\xe4\x93\x02,\x12*/cosmwasm/wasm/v1/contract/{address}/state\x12\xa9\x01\n\x10RawContractState\x12..cosmwasm.wasm.v1.QueryRawContractStateRequest\x1a/.cosmwasm.wasm.v1.QueryRawContractStateResponse\"4\x82\xd3\xe4\x93\x02.\x12,/wasm/v1/contract/{address}/raw/{query_data}\x12\xb1\x01\n\x12SmartContractState\x12\x30.cosmwasm.wasm.v1.QuerySmartContractStateRequest\x1a\x31.cosmwasm.wasm.v1.QuerySmartContractStateResponse\"6\x82\xd3\xe4\x93\x02\x30\x12./wasm/v1/contract/{address}/smart/{query_data}\x12y\n\x04\x43ode\x12\".cosmwasm.wasm.v1.QueryCodeRequest\x1a#.cosmwasm.wasm.v1.QueryCodeResponse\"(\x82\xd3\xe4\x93\x02\"\x12 /cosmwasm/wasm/v1/code/{code_id}\x12r\n\x05\x43odes\x12#.cosmwasm.wasm.v1.QueryCodesRequest\x1a$.cosmwasm.wasm.v1.QueryCodesResponse\"\x1e\x82\xd3\xe4\x93\x02\x18\x12\x16/cosmwasm/wasm/v1/code\x12\x8c\x01\n\x0bPinnedCodes\x12).cosmwasm.wasm.v1.QueryPinnedCodesRequest\x1a*.cosmwasm.wasm.v1.QueryPinnedCodesResponse\"&\x82\xd3\xe4\x93\x02 \x12\x1e/cosmwasm/wasm/v1/codes/pinnedB0Z&github.com/CosmWasm/wasmd/x/wasm/types\xc8\xe1\x1e\x00\xa8\xe2\x1e\x00\x62\x06proto3')



_QUERYCONTRACTINFOREQUEST = DESCRIPTOR.message_types_by_name['QueryContractInfoRequest']
_QUERYCONTRACTINFORESPONSE = DESCRIPTOR.message_types_by_name['QueryContractInfoResponse']
_QUERYCONTRACTHISTORYREQUEST = DESCRIPTOR.message_types_by_name['QueryContractHistoryRequest']
_QUERYCONTRACTHISTORYRESPONSE = DESCRIPTOR.message_types_by_name['QueryContractHistoryResponse']
_QUERYCONTRACTSBYCODEREQUEST = DESCRIPTOR.message_types_by_name['QueryContractsByCodeRequest']
_QUERYCONTRACTSBYCODERESPONSE = DESCRIPTOR.message_types_by_name['QueryContractsByCodeResponse']
_QUERYALLCONTRACTSTATEREQUEST = DESCRIPTOR.message_types_by_name['QueryAllContractStateRequest']
_QUERYALLCONTRACTSTATERESPONSE = DESCRIPTOR.message_types_by_name['QueryAllContractStateResponse']
_QUERYRAWCONTRACTSTATEREQUEST = DESCRIPTOR.message_types_by_name['QueryRawContractStateRequest']
_QUERYRAWCONTRACTSTATERESPONSE = DESCRIPTOR.message_types_by_name['QueryRawContractStateResponse']
_QUERYSMARTCONTRACTSTATEREQUEST = DESCRIPTOR.message_types_by_name['QuerySmartContractStateRequest']
_QUERYSMARTCONTRACTSTATERESPONSE = DESCRIPTOR.message_types_by_name['QuerySmartContractStateResponse']
_QUERYCODEREQUEST = DESCRIPTOR.message_types_by_name['QueryCodeRequest']
_CODEINFORESPONSE = DESCRIPTOR.message_types_by_name['CodeInfoResponse']
_QUERYCODERESPONSE = DESCRIPTOR.message_types_by_name['QueryCodeResponse']
_QUERYCODESREQUEST = DESCRIPTOR.message_types_by_name['QueryCodesRequest']
_QUERYCODESRESPONSE = DESCRIPTOR.message_types_by_name['QueryCodesResponse']
_QUERYPINNEDCODESREQUEST = DESCRIPTOR.message_types_by_name['QueryPinnedCodesRequest']
_QUERYPINNEDCODESRESPONSE = DESCRIPTOR.message_types_by_name['QueryPinnedCodesResponse']
QueryContractInfoRequest = _reflection.GeneratedProtocolMessageType('QueryContractInfoRequest', (_message.Message,), {
  'DESCRIPTOR' : _QUERYCONTRACTINFOREQUEST,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryContractInfoRequest)
  })
_sym_db.RegisterMessage(QueryContractInfoRequest)

QueryContractInfoResponse = _reflection.GeneratedProtocolMessageType('QueryContractInfoResponse', (_message.Message,), {
  'DESCRIPTOR' : _QUERYCONTRACTINFORESPONSE,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryContractInfoResponse)
  })
_sym_db.RegisterMessage(QueryContractInfoResponse)

QueryContractHistoryRequest = _reflection.GeneratedProtocolMessageType('QueryContractHistoryRequest', (_message.Message,), {
  'DESCRIPTOR' : _QUERYCONTRACTHISTORYREQUEST,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryContractHistoryRequest)
  })
_sym_db.RegisterMessage(QueryContractHistoryRequest)

QueryContractHistoryResponse = _reflection.GeneratedProtocolMessageType('QueryContractHistoryResponse', (_message.Message,), {
  'DESCRIPTOR' : _QUERYCONTRACTHISTORYRESPONSE,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryContractHistoryResponse)
  })
_sym_db.RegisterMessage(QueryContractHistoryResponse)

QueryContractsByCodeRequest = _reflection.GeneratedProtocolMessageType('QueryContractsByCodeRequest', (_message.Message,), {
  'DESCRIPTOR' : _QUERYCONTRACTSBYCODEREQUEST,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryContractsByCodeRequest)
  })
_sym_db.RegisterMessage(QueryContractsByCodeRequest)

QueryContractsByCodeResponse = _reflection.GeneratedProtocolMessageType('QueryContractsByCodeResponse', (_message.Message,), {
  'DESCRIPTOR' : _QUERYCONTRACTSBYCODERESPONSE,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryContractsByCodeResponse)
  })
_sym_db.RegisterMessage(QueryContractsByCodeResponse)

QueryAllContractStateRequest = _reflection.GeneratedProtocolMessageType('QueryAllContractStateRequest', (_message.Message,), {
  'DESCRIPTOR' : _QUERYALLCONTRACTSTATEREQUEST,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryAllContractStateRequest)
  })
_sym_db.RegisterMessage(QueryAllContractStateRequest)

QueryAllContractStateResponse = _reflection.GeneratedProtocolMessageType('QueryAllContractStateResponse', (_message.Message,), {
  'DESCRIPTOR' : _QUERYALLCONTRACTSTATERESPONSE,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryAllContractStateResponse)
  })
_sym_db.RegisterMessage(QueryAllContractStateResponse)

QueryRawContractStateRequest = _reflection.GeneratedProtocolMessageType('QueryRawContractStateRequest', (_message.Message,), {
  'DESCRIPTOR' : _QUERYRAWCONTRACTSTATEREQUEST,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryRawContractStateRequest)
  })
_sym_db.RegisterMessage(QueryRawContractStateRequest)

QueryRawContractStateResponse = _reflection.GeneratedProtocolMessageType('QueryRawContractStateResponse', (_message.Message,), {
  'DESCRIPTOR' : _QUERYRAWCONTRACTSTATERESPONSE,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryRawContractStateResponse)
  })
_sym_db.RegisterMessage(QueryRawContractStateResponse)

QuerySmartContractStateRequest = _reflection.GeneratedProtocolMessageType('QuerySmartContractStateRequest', (_message.Message,), {
  'DESCRIPTOR' : _QUERYSMARTCONTRACTSTATEREQUEST,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QuerySmartContractStateRequest)
  })
_sym_db.RegisterMessage(QuerySmartContractStateRequest)

QuerySmartContractStateResponse = _reflection.GeneratedProtocolMessageType('QuerySmartContractStateResponse', (_message.Message,), {
  'DESCRIPTOR' : _QUERYSMARTCONTRACTSTATERESPONSE,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QuerySmartContractStateResponse)
  })
_sym_db.RegisterMessage(QuerySmartContractStateResponse)

QueryCodeRequest = _reflection.GeneratedProtocolMessageType('QueryCodeRequest', (_message.Message,), {
  'DESCRIPTOR' : _QUERYCODEREQUEST,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryCodeRequest)
  })
_sym_db.RegisterMessage(QueryCodeRequest)

CodeInfoResponse = _reflection.GeneratedProtocolMessageType('CodeInfoResponse', (_message.Message,), {
  'DESCRIPTOR' : _CODEINFORESPONSE,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.CodeInfoResponse)
  })
_sym_db.RegisterMessage(CodeInfoResponse)

QueryCodeResponse = _reflection.GeneratedProtocolMessageType('QueryCodeResponse', (_message.Message,), {
  'DESCRIPTOR' : _QUERYCODERESPONSE,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryCodeResponse)
  })
_sym_db.RegisterMessage(QueryCodeResponse)

QueryCodesRequest = _reflection.GeneratedProtocolMessageType('QueryCodesRequest', (_message.Message,), {
  'DESCRIPTOR' : _QUERYCODESREQUEST,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryCodesRequest)
  })
_sym_db.RegisterMessage(QueryCodesRequest)

QueryCodesResponse = _reflection.GeneratedProtocolMessageType('QueryCodesResponse', (_message.Message,), {
  'DESCRIPTOR' : _QUERYCODESRESPONSE,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryCodesResponse)
  })
_sym_db.RegisterMessage(QueryCodesResponse)

QueryPinnedCodesRequest = _reflection.GeneratedProtocolMessageType('QueryPinnedCodesRequest', (_message.Message,), {
  'DESCRIPTOR' : _QUERYPINNEDCODESREQUEST,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryPinnedCodesRequest)
  })
_sym_db.RegisterMessage(QueryPinnedCodesRequest)

QueryPinnedCodesResponse = _reflection.GeneratedProtocolMessageType('QueryPinnedCodesResponse', (_message.Message,), {
  'DESCRIPTOR' : _QUERYPINNEDCODESRESPONSE,
  '__module__' : 'cosmwasm.wasm.v1.query_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1.QueryPinnedCodesResponse)
  })
_sym_db.RegisterMessage(QueryPinnedCodesResponse)

_QUERY = DESCRIPTOR.services_by_name['Query']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z&github.com/CosmWasm/wasmd/x/wasm/types\310\341\036\000\250\342\036\000'
  _QUERYCONTRACTINFORESPONSE.fields_by_name['contract_info']._options = None
  _QUERYCONTRACTINFORESPONSE.fields_by_name['contract_info']._serialized_options = b'\320\336\037\001\310\336\037\000\352\336\037\000'
  _QUERYCONTRACTINFORESPONSE._options = None
  _QUERYCONTRACTINFORESPONSE._serialized_options = b'\350\240\037\001'
  _QUERYCONTRACTHISTORYRESPONSE.fields_by_name['entries']._options = None
  _QUERYCONTRACTHISTORYRESPONSE.fields_by_name['entries']._serialized_options = b'\310\336\037\000'
  _QUERYALLCONTRACTSTATERESPONSE.fields_by_name['models']._options = None
  _QUERYALLCONTRACTSTATERESPONSE.fields_by_name['models']._serialized_options = b'\310\336\037\000'
  _QUERYSMARTCONTRACTSTATEREQUEST.fields_by_name['query_data']._options = None
  _QUERYSMARTCONTRACTSTATEREQUEST.fields_by_name['query_data']._serialized_options = b'\372\336\037\022RawContractMessage'
  _QUERYSMARTCONTRACTSTATERESPONSE.fields_by_name['data']._options = None
  _QUERYSMARTCONTRACTSTATERESPONSE.fields_by_name['data']._serialized_options = b'\372\336\037\022RawContractMessage'
  _CODEINFORESPONSE.fields_by_name['code_id']._options = None
  _CODEINFORESPONSE.fields_by_name['code_id']._serialized_options = b'\342\336\037\006CodeID\352\336\037\002id'
  _CODEINFORESPONSE.fields_by_name['data_hash']._options = None
  _CODEINFORESPONSE.fields_by_name['data_hash']._serialized_options = b'\372\336\0374github.com/tendermint/tendermint/libs/bytes.HexBytes'
  _CODEINFORESPONSE._options = None
  _CODEINFORESPONSE._serialized_options = b'\350\240\037\001'
  _QUERYCODERESPONSE.fields_by_name['code_info']._options = None
  _QUERYCODERESPONSE.fields_by_name['code_info']._serialized_options = b'\320\336\037\001\352\336\037\000'
  _QUERYCODERESPONSE.fields_by_name['data']._options = None
  _QUERYCODERESPONSE.fields_by_name['data']._serialized_options = b'\352\336\037\004data'
  _QUERYCODERESPONSE._options = None
  _QUERYCODERESPONSE._serialized_options = b'\350\240\037\001'
  _QUERYCODESRESPONSE.fields_by_name['code_infos']._options = None
  _QUERYCODESRESPONSE.fields_by_name['code_infos']._serialized_options = b'\310\336\037\000'
  _QUERYPINNEDCODESRESPONSE.fields_by_name['code_ids']._options = None
  _QUERYPINNEDCODESRESPONSE.fields_by_name['code_ids']._serialized_options = b'\310\336\037\000\342\336\037\007CodeIDs'
  _QUERY.methods_by_name['ContractInfo']._options = None
  _QUERY.methods_by_name['ContractInfo']._serialized_options = b'\202\323\344\223\002&\022$/cosmwasm/wasm/v1/contract/{address}'
  _QUERY.methods_by_name['ContractHistory']._options = None
  _QUERY.methods_by_name['ContractHistory']._serialized_options = b'\202\323\344\223\002.\022,/cosmwasm/wasm/v1/contract/{address}/history'
  _QUERY.methods_by_name['ContractsByCode']._options = None
  _QUERY.methods_by_name['ContractsByCode']._serialized_options = b'\202\323\344\223\002,\022*/cosmwasm/wasm/v1/code/{code_id}/contracts'
  _QUERY.methods_by_name['AllContractState']._options = None
  _QUERY.methods_by_name['AllContractState']._serialized_options = b'\202\323\344\223\002,\022*/cosmwasm/wasm/v1/contract/{address}/state'
  _QUERY.methods_by_name['RawContractState']._options = None
  _QUERY.methods_by_name['RawContractState']._serialized_options = b'\202\323\344\223\002.\022,/wasm/v1/contract/{address}/raw/{query_data}'
  _QUERY.methods_by_name['SmartContractState']._options = None
  _QUERY.methods_by_name['SmartContractState']._serialized_options = b'\202\323\344\223\0020\022./wasm/v1/contract/{address}/smart/{query_data}'
  _QUERY.methods_by_name['Code']._options = None
  _QUERY.methods_by_name['Code']._serialized_options = b'\202\323\344\223\002\"\022 /cosmwasm/wasm/v1/code/{code_id}'
  _QUERY.methods_by_name['Codes']._options = None
  _QUERY.methods_by_name['Codes']._serialized_options = b'\202\323\344\223\002\030\022\026/cosmwasm/wasm/v1/code'
  _QUERY.methods_by_name['PinnedCodes']._options = None
  _QUERY.methods_by_name['PinnedCodes']._serialized_options = b'\202\323\344\223\002 \022\036/cosmwasm/wasm/v1/codes/pinned'
  _QUERYCONTRACTINFOREQUEST._serialized_start=176
  _QUERYCONTRACTINFOREQUEST._serialized_end=219
  _QUERYCONTRACTINFORESPONSE._serialized_start=221
  _QUERYCONTRACTINFORESPONSE._serialized_end=340
  _QUERYCONTRACTHISTORYREQUEST._serialized_start=342
  _QUERYCONTRACTHISTORYREQUEST._serialized_end=448
  _QUERYCONTRACTHISTORYRESPONSE._serialized_start=451
  _QUERYCONTRACTHISTORYRESPONSE._serialized_end=609
  _QUERYCONTRACTSBYCODEREQUEST._serialized_start=611
  _QUERYCONTRACTSBYCODEREQUEST._serialized_end=717
  _QUERYCONTRACTSBYCODERESPONSE._serialized_start=719
  _QUERYCONTRACTSBYCODERESPONSE._serialized_end=829
  _QUERYALLCONTRACTSTATEREQUEST._serialized_start=831
  _QUERYALLCONTRACTSTATEREQUEST._serialized_end=938
  _QUERYALLCONTRACTSTATERESPONSE._serialized_start=941
  _QUERYALLCONTRACTSTATERESPONSE._serialized_end=1080
  _QUERYRAWCONTRACTSTATEREQUEST._serialized_start=1082
  _QUERYRAWCONTRACTSTATEREQUEST._serialized_end=1149
  _QUERYRAWCONTRACTSTATERESPONSE._serialized_start=1151
  _QUERYRAWCONTRACTSTATERESPONSE._serialized_end=1196
  _QUERYSMARTCONTRACTSTATEREQUEST._serialized_start=1198
  _QUERYSMARTCONTRACTSTATEREQUEST._serialized_end=1291
  _QUERYSMARTCONTRACTSTATERESPONSE._serialized_start=1293
  _QUERYSMARTCONTRACTSTATERESPONSE._serialized_end=1364
  _QUERYCODEREQUEST._serialized_start=1366
  _QUERYCODEREQUEST._serialized_end=1401
  _CODEINFORESPONSE._serialized_start=1404
  _CODEINFORESPONSE._serialized_end=1569
  _QUERYCODERESPONSE._serialized_start=1571
  _QUERYCODERESPONSE._serialized_end=1685
  _QUERYCODESREQUEST._serialized_start=1687
  _QUERYCODESREQUEST._serialized_end=1766
  _QUERYCODESRESPONSE._serialized_start=1769
  _QUERYCODESRESPONSE._serialized_end=1912
  _QUERYPINNEDCODESREQUEST._serialized_start=1914
  _QUERYPINNEDCODESREQUEST._serialized_end=1999
  _QUERYPINNEDCODESRESPONSE._serialized_start=2001
  _QUERYPINNEDCODESRESPONSE._serialized_end=2123
  _QUERY._serialized_start=2126
  _QUERY._serialized_end=3525
# @@protoc_insertion_point(module_scope)
