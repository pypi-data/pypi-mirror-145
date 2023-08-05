# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmwasm/wasm/v1beta1/proposal.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from cosmwasm.wasm.v1beta1 import types_pb2 as cosmwasm_dot_wasm_dot_v1beta1_dot_types__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='cosmwasm/wasm/v1beta1/proposal.proto',
  package='cosmwasm.wasm.v1beta1',
  syntax='proto3',
  serialized_options=b'Z&github.com/CosmWasm/wasmd/x/wasm/types\330\341\036\000\310\341\036\000\250\342\036\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n$cosmwasm/wasm/v1beta1/proposal.proto\x12\x15\x63osmwasm.wasm.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1e\x63osmos/base/v1beta1/coin.proto\x1a!cosmwasm/wasm/v1beta1/types.proto\"\xd7\x01\n\x11StoreCodeProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x0e\n\x06run_as\x18\x03 \x01(\t\x12(\n\x0ewasm_byte_code\x18\x04 \x01(\x0c\x42\x10\xe2\xde\x1f\x0cWASMByteCode\x12\x0e\n\x06source\x18\x05 \x01(\t\x12\x0f\n\x07\x62uilder\x18\x06 \x01(\t\x12\x43\n\x16instantiate_permission\x18\x07 \x01(\x0b\x32#.cosmwasm.wasm.v1beta1.AccessConfig\"\x98\x02\n\x1bInstantiateContractProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x0e\n\x06run_as\x18\x03 \x01(\t\x12\r\n\x05\x61\x64min\x18\x04 \x01(\t\x12\x1b\n\x07\x63ode_id\x18\x05 \x01(\x04\x42\n\xe2\xde\x1f\x06\x43odeID\x12\r\n\x05label\x18\x06 \x01(\t\x12.\n\x08init_msg\x18\x07 \x01(\x0c\x42\x1c\xfa\xde\x1f\x18\x65ncoding/json.RawMessage\x12Z\n\x05\x66unds\x18\x08 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\"\xaf\x01\n\x17MigrateContractProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x0e\n\x06run_as\x18\x03 \x01(\t\x12\x10\n\x08\x63ontract\x18\x04 \x01(\t\x12\x1b\n\x07\x63ode_id\x18\x05 \x01(\x04\x42\n\xe2\xde\x1f\x06\x43odeID\x12\x31\n\x0bmigrate_msg\x18\x06 \x01(\x0c\x42\x1c\xfa\xde\x1f\x18\x65ncoding/json.RawMessage\"t\n\x13UpdateAdminProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\'\n\tnew_admin\x18\x03 \x01(\tB\x14\xf2\xde\x1f\x10yaml:\"new_admin\"\x12\x10\n\x08\x63ontract\x18\x04 \x01(\t\"J\n\x12\x43learAdminProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x10\n\x08\x63ontract\x18\x03 \x01(\t\"\x92\x01\n\x10PinCodesProposal\x12\x1f\n\x05title\x18\x01 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:\"title\"\x12+\n\x0b\x64\x65scription\x18\x02 \x01(\tB\x16\xf2\xde\x1f\x12yaml:\"description\"\x12\x30\n\x08\x63ode_ids\x18\x03 \x03(\x04\x42\x1e\xe2\xde\x1f\x07\x43odeIDs\xf2\xde\x1f\x0fyaml:\"code_ids\"\"\x94\x01\n\x12UnpinCodesProposal\x12\x1f\n\x05title\x18\x01 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:\"title\"\x12+\n\x0b\x64\x65scription\x18\x02 \x01(\tB\x16\xf2\xde\x1f\x12yaml:\"description\"\x12\x30\n\x08\x63ode_ids\x18\x03 \x03(\x04\x42\x1e\xe2\xde\x1f\x07\x43odeIDs\xf2\xde\x1f\x0fyaml:\"code_ids\"B4Z&github.com/CosmWasm/wasmd/x/wasm/types\xd8\xe1\x1e\x00\xc8\xe1\x1e\x00\xa8\xe2\x1e\x01\x62\x06proto3'
  ,
  dependencies=[gogoproto_dot_gogo__pb2.DESCRIPTOR,cosmos_dot_base_dot_v1beta1_dot_coin__pb2.DESCRIPTOR,cosmwasm_dot_wasm_dot_v1beta1_dot_types__pb2.DESCRIPTOR,])




_STORECODEPROPOSAL = _descriptor.Descriptor(
  name='StoreCodeProposal',
  full_name='cosmwasm.wasm.v1beta1.StoreCodeProposal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='cosmwasm.wasm.v1beta1.StoreCodeProposal.title', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='cosmwasm.wasm.v1beta1.StoreCodeProposal.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='run_as', full_name='cosmwasm.wasm.v1beta1.StoreCodeProposal.run_as', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='wasm_byte_code', full_name='cosmwasm.wasm.v1beta1.StoreCodeProposal.wasm_byte_code', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\342\336\037\014WASMByteCode', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='source', full_name='cosmwasm.wasm.v1beta1.StoreCodeProposal.source', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='builder', full_name='cosmwasm.wasm.v1beta1.StoreCodeProposal.builder', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='instantiate_permission', full_name='cosmwasm.wasm.v1beta1.StoreCodeProposal.instantiate_permission', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=153,
  serialized_end=368,
)


_INSTANTIATECONTRACTPROPOSAL = _descriptor.Descriptor(
  name='InstantiateContractProposal',
  full_name='cosmwasm.wasm.v1beta1.InstantiateContractProposal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='cosmwasm.wasm.v1beta1.InstantiateContractProposal.title', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='cosmwasm.wasm.v1beta1.InstantiateContractProposal.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='run_as', full_name='cosmwasm.wasm.v1beta1.InstantiateContractProposal.run_as', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='admin', full_name='cosmwasm.wasm.v1beta1.InstantiateContractProposal.admin', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='code_id', full_name='cosmwasm.wasm.v1beta1.InstantiateContractProposal.code_id', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\342\336\037\006CodeID', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='label', full_name='cosmwasm.wasm.v1beta1.InstantiateContractProposal.label', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='init_msg', full_name='cosmwasm.wasm.v1beta1.InstantiateContractProposal.init_msg', index=6,
      number=7, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372\336\037\030encoding/json.RawMessage', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='funds', full_name='cosmwasm.wasm.v1beta1.InstantiateContractProposal.funds', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\310\336\037\000\252\337\037(github.com/cosmos/cosmos-sdk/types.Coins', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=371,
  serialized_end=651,
)


_MIGRATECONTRACTPROPOSAL = _descriptor.Descriptor(
  name='MigrateContractProposal',
  full_name='cosmwasm.wasm.v1beta1.MigrateContractProposal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='cosmwasm.wasm.v1beta1.MigrateContractProposal.title', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='cosmwasm.wasm.v1beta1.MigrateContractProposal.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='run_as', full_name='cosmwasm.wasm.v1beta1.MigrateContractProposal.run_as', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='contract', full_name='cosmwasm.wasm.v1beta1.MigrateContractProposal.contract', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='code_id', full_name='cosmwasm.wasm.v1beta1.MigrateContractProposal.code_id', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\342\336\037\006CodeID', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='migrate_msg', full_name='cosmwasm.wasm.v1beta1.MigrateContractProposal.migrate_msg', index=5,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372\336\037\030encoding/json.RawMessage', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=654,
  serialized_end=829,
)


_UPDATEADMINPROPOSAL = _descriptor.Descriptor(
  name='UpdateAdminProposal',
  full_name='cosmwasm.wasm.v1beta1.UpdateAdminProposal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='cosmwasm.wasm.v1beta1.UpdateAdminProposal.title', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='cosmwasm.wasm.v1beta1.UpdateAdminProposal.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='new_admin', full_name='cosmwasm.wasm.v1beta1.UpdateAdminProposal.new_admin', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\362\336\037\020yaml:\"new_admin\"', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='contract', full_name='cosmwasm.wasm.v1beta1.UpdateAdminProposal.contract', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=831,
  serialized_end=947,
)


_CLEARADMINPROPOSAL = _descriptor.Descriptor(
  name='ClearAdminProposal',
  full_name='cosmwasm.wasm.v1beta1.ClearAdminProposal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='cosmwasm.wasm.v1beta1.ClearAdminProposal.title', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='cosmwasm.wasm.v1beta1.ClearAdminProposal.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='contract', full_name='cosmwasm.wasm.v1beta1.ClearAdminProposal.contract', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=949,
  serialized_end=1023,
)


_PINCODESPROPOSAL = _descriptor.Descriptor(
  name='PinCodesProposal',
  full_name='cosmwasm.wasm.v1beta1.PinCodesProposal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='cosmwasm.wasm.v1beta1.PinCodesProposal.title', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\362\336\037\014yaml:\"title\"', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='cosmwasm.wasm.v1beta1.PinCodesProposal.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\362\336\037\022yaml:\"description\"', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='code_ids', full_name='cosmwasm.wasm.v1beta1.PinCodesProposal.code_ids', index=2,
      number=3, type=4, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\342\336\037\007CodeIDs\362\336\037\017yaml:\"code_ids\"', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1026,
  serialized_end=1172,
)


_UNPINCODESPROPOSAL = _descriptor.Descriptor(
  name='UnpinCodesProposal',
  full_name='cosmwasm.wasm.v1beta1.UnpinCodesProposal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='cosmwasm.wasm.v1beta1.UnpinCodesProposal.title', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\362\336\037\014yaml:\"title\"', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='cosmwasm.wasm.v1beta1.UnpinCodesProposal.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\362\336\037\022yaml:\"description\"', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='code_ids', full_name='cosmwasm.wasm.v1beta1.UnpinCodesProposal.code_ids', index=2,
      number=3, type=4, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\342\336\037\007CodeIDs\362\336\037\017yaml:\"code_ids\"', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1175,
  serialized_end=1323,
)

_STORECODEPROPOSAL.fields_by_name['instantiate_permission'].message_type = cosmwasm_dot_wasm_dot_v1beta1_dot_types__pb2._ACCESSCONFIG
_INSTANTIATECONTRACTPROPOSAL.fields_by_name['funds'].message_type = cosmos_dot_base_dot_v1beta1_dot_coin__pb2._COIN
DESCRIPTOR.message_types_by_name['StoreCodeProposal'] = _STORECODEPROPOSAL
DESCRIPTOR.message_types_by_name['InstantiateContractProposal'] = _INSTANTIATECONTRACTPROPOSAL
DESCRIPTOR.message_types_by_name['MigrateContractProposal'] = _MIGRATECONTRACTPROPOSAL
DESCRIPTOR.message_types_by_name['UpdateAdminProposal'] = _UPDATEADMINPROPOSAL
DESCRIPTOR.message_types_by_name['ClearAdminProposal'] = _CLEARADMINPROPOSAL
DESCRIPTOR.message_types_by_name['PinCodesProposal'] = _PINCODESPROPOSAL
DESCRIPTOR.message_types_by_name['UnpinCodesProposal'] = _UNPINCODESPROPOSAL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StoreCodeProposal = _reflection.GeneratedProtocolMessageType('StoreCodeProposal', (_message.Message,), {
  'DESCRIPTOR' : _STORECODEPROPOSAL,
  '__module__' : 'cosmwasm.wasm.v1beta1.proposal_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1beta1.StoreCodeProposal)
  })
_sym_db.RegisterMessage(StoreCodeProposal)

InstantiateContractProposal = _reflection.GeneratedProtocolMessageType('InstantiateContractProposal', (_message.Message,), {
  'DESCRIPTOR' : _INSTANTIATECONTRACTPROPOSAL,
  '__module__' : 'cosmwasm.wasm.v1beta1.proposal_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1beta1.InstantiateContractProposal)
  })
_sym_db.RegisterMessage(InstantiateContractProposal)

MigrateContractProposal = _reflection.GeneratedProtocolMessageType('MigrateContractProposal', (_message.Message,), {
  'DESCRIPTOR' : _MIGRATECONTRACTPROPOSAL,
  '__module__' : 'cosmwasm.wasm.v1beta1.proposal_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1beta1.MigrateContractProposal)
  })
_sym_db.RegisterMessage(MigrateContractProposal)

UpdateAdminProposal = _reflection.GeneratedProtocolMessageType('UpdateAdminProposal', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEADMINPROPOSAL,
  '__module__' : 'cosmwasm.wasm.v1beta1.proposal_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1beta1.UpdateAdminProposal)
  })
_sym_db.RegisterMessage(UpdateAdminProposal)

ClearAdminProposal = _reflection.GeneratedProtocolMessageType('ClearAdminProposal', (_message.Message,), {
  'DESCRIPTOR' : _CLEARADMINPROPOSAL,
  '__module__' : 'cosmwasm.wasm.v1beta1.proposal_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1beta1.ClearAdminProposal)
  })
_sym_db.RegisterMessage(ClearAdminProposal)

PinCodesProposal = _reflection.GeneratedProtocolMessageType('PinCodesProposal', (_message.Message,), {
  'DESCRIPTOR' : _PINCODESPROPOSAL,
  '__module__' : 'cosmwasm.wasm.v1beta1.proposal_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1beta1.PinCodesProposal)
  })
_sym_db.RegisterMessage(PinCodesProposal)

UnpinCodesProposal = _reflection.GeneratedProtocolMessageType('UnpinCodesProposal', (_message.Message,), {
  'DESCRIPTOR' : _UNPINCODESPROPOSAL,
  '__module__' : 'cosmwasm.wasm.v1beta1.proposal_pb2'
  # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1beta1.UnpinCodesProposal)
  })
_sym_db.RegisterMessage(UnpinCodesProposal)


DESCRIPTOR._options = None
_STORECODEPROPOSAL.fields_by_name['wasm_byte_code']._options = None
_INSTANTIATECONTRACTPROPOSAL.fields_by_name['code_id']._options = None
_INSTANTIATECONTRACTPROPOSAL.fields_by_name['init_msg']._options = None
_INSTANTIATECONTRACTPROPOSAL.fields_by_name['funds']._options = None
_MIGRATECONTRACTPROPOSAL.fields_by_name['code_id']._options = None
_MIGRATECONTRACTPROPOSAL.fields_by_name['migrate_msg']._options = None
_UPDATEADMINPROPOSAL.fields_by_name['new_admin']._options = None
_PINCODESPROPOSAL.fields_by_name['title']._options = None
_PINCODESPROPOSAL.fields_by_name['description']._options = None
_PINCODESPROPOSAL.fields_by_name['code_ids']._options = None
_UNPINCODESPROPOSAL.fields_by_name['title']._options = None
_UNPINCODESPROPOSAL.fields_by_name['description']._options = None
_UNPINCODESPROPOSAL.fields_by_name['code_ids']._options = None
# @@protoc_insertion_point(module_scope)
