# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: goroda.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'goroda.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cgoroda.proto\"2\n\rClientMessage\x12\x13\n\x0bplayer_name\x18\x01 \x01(\t\x12\x0c\n\x04\x63ity\x18\x02 \x01(\t\"V\n\rServerMessage\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x13\n\x0bnext_letter\x18\x03 \x01(\t\x12\x0f\n\x07is_turn\x18\x04 \x01(\x08\x32<\n\nGorodaGame\x12.\n\x08JoinGame\x12\x0e.ClientMessage\x1a\x0e.ServerMessage(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'goroda_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CLIENTMESSAGE']._serialized_start=16
  _globals['_CLIENTMESSAGE']._serialized_end=66
  _globals['_SERVERMESSAGE']._serialized_start=68
  _globals['_SERVERMESSAGE']._serialized_end=154
  _globals['_GORODAGAME']._serialized_start=156
  _globals['_GORODAGAME']._serialized_end=216
# @@protoc_insertion_point(module_scope)
