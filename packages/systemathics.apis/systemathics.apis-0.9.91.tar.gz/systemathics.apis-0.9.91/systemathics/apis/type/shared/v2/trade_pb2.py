# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: systemathics/apis/type/shared/v2/trade.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,systemathics/apis/type/shared/v2/trade.proto\x12 systemathics.apis.type.shared.v2\"C\n\x05Trade\x12\r\n\x05price\x18\x01 \x01(\x01\x12\x0c\n\x04size\x18\x02 \x01(\x03\x12\x11\n\tcondition\x18\x03 \x01(\t\x12\n\n\x02id\x18\x04 \x01(\tb\x06proto3')



_TRADE = DESCRIPTOR.message_types_by_name['Trade']
Trade = _reflection.GeneratedProtocolMessageType('Trade', (_message.Message,), {
  'DESCRIPTOR' : _TRADE,
  '__module__' : 'systemathics.apis.type.shared.v2.trade_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.type.shared.v2.Trade)
  })
_sym_db.RegisterMessage(Trade)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TRADE._serialized_start=82
  _TRADE._serialized_end=149
# @@protoc_insertion_point(module_scope)
