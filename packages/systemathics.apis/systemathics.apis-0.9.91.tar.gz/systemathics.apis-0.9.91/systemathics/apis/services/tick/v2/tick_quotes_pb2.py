# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: systemathics/apis/services/tick/v2/tick_quotes.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from systemathics.apis.type.shared.v1 import constraints_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2
from systemathics.apis.type.shared.v1 import identifier_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2
from systemathics.apis.type.shared.v1 import keys_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_keys__pb2
from systemathics.apis.type.shared.v2 import quotes_data_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v2_dot_quotes__data__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n4systemathics/apis/services/tick/v2/tick_quotes.proto\x12\"systemathics.apis.services.tick.v2\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x32systemathics/apis/type/shared/v1/constraints.proto\x1a\x31systemathics/apis/type/shared/v1/identifier.proto\x1a+systemathics/apis/type/shared/v1/keys.proto\x1a\x32systemathics/apis/type/shared/v2/quotes_data.proto\"\xae\x01\n\x11TickQuotesRequest\x12\x41\n\x0bidentifiers\x18\x01 \x03(\x0b\x32,.systemathics.apis.type.shared.v1.Identifier\x12\x42\n\x0b\x63onstraints\x18\x02 \x01(\x0b\x32-.systemathics.apis.type.shared.v1.Constraints\x12\x12\n\nadjustment\x18\x03 \x01(\x08\"\x98\x01\n\x12TickQuotesResponse\x12<\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32,.systemathics.apis.type.shared.v2.QuotesDataH\x00\x12\x39\n\x07mapping\x18\x02 \x01(\x0b\x32&.systemathics.apis.type.shared.v1.KeysH\x00\x42\t\n\x07payload2\x92\x01\n\x11TickQuotesService\x12}\n\nTickQuotes\x12\x35.systemathics.apis.services.tick.v2.TickQuotesRequest\x1a\x36.systemathics.apis.services.tick.v2.TickQuotesResponse0\x01\x62\x06proto3')



_TICKQUOTESREQUEST = DESCRIPTOR.message_types_by_name['TickQuotesRequest']
_TICKQUOTESRESPONSE = DESCRIPTOR.message_types_by_name['TickQuotesResponse']
TickQuotesRequest = _reflection.GeneratedProtocolMessageType('TickQuotesRequest', (_message.Message,), {
  'DESCRIPTOR' : _TICKQUOTESREQUEST,
  '__module__' : 'systemathics.apis.services.tick.v2.tick_quotes_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.tick.v2.TickQuotesRequest)
  })
_sym_db.RegisterMessage(TickQuotesRequest)

TickQuotesResponse = _reflection.GeneratedProtocolMessageType('TickQuotesResponse', (_message.Message,), {
  'DESCRIPTOR' : _TICKQUOTESRESPONSE,
  '__module__' : 'systemathics.apis.services.tick.v2.tick_quotes_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.tick.v2.TickQuotesResponse)
  })
_sym_db.RegisterMessage(TickQuotesResponse)

_TICKQUOTESSERVICE = DESCRIPTOR.services_by_name['TickQuotesService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TICKQUOTESREQUEST._serialized_start=358
  _TICKQUOTESREQUEST._serialized_end=532
  _TICKQUOTESRESPONSE._serialized_start=535
  _TICKQUOTESRESPONSE._serialized_end=687
  _TICKQUOTESSERVICE._serialized_start=690
  _TICKQUOTESSERVICE._serialized_end=836
# @@protoc_insertion_point(module_scope)
