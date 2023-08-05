# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: systemathics/apis/services/intraday/v1/intraday_vwap.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from systemathics.apis.type.shared.v1 import identifier_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2
from systemathics.apis.type.shared.v1 import constraints_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2
from systemathics.apis.type.shared.v1 import sampling_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_sampling__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n:systemathics/apis/services/intraday/v1/intraday_vwap.proto\x12&systemathics.apis.services.intraday.v1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x31systemathics/apis/type/shared/v1/identifier.proto\x1a\x32systemathics/apis/type/shared/v1/constraints.proto\x1a/systemathics/apis/type/shared/v1/sampling.proto\"\xee\x01\n\x14IntradayVwapsRequest\x12@\n\nidentifier\x18\x01 \x01(\x0b\x32,.systemathics.apis.type.shared.v1.Identifier\x12<\n\x08sampling\x18\x02 \x01(\x0e\x32*.systemathics.apis.type.shared.v1.Sampling\x12\x42\n\x0b\x63onstraints\x18\x03 \x01(\x0b\x32-.systemathics.apis.type.shared.v1.Constraints\x12\x12\n\nadjustment\x18\x04 \x01(\x08\"[\n\x15IntradayVwapsResponse\x12\x42\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x34.systemathics.apis.services.intraday.v1.IntradayVwap\"l\n\x0cIntradayVwap\x12.\n\ntime_stamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05price\x18\x02 \x01(\x01\x12\x0e\n\x06volume\x18\x03 \x01(\x03\x12\r\n\x05score\x18\x04 \x01(\x01\x32\xa5\x01\n\x14IntradayVwapsService\x12\x8c\x01\n\rIntradayVwaps\x12<.systemathics.apis.services.intraday.v1.IntradayVwapsRequest\x1a=.systemathics.apis.services.intraday.v1.IntradayVwapsResponseb\x06proto3')



_INTRADAYVWAPSREQUEST = DESCRIPTOR.message_types_by_name['IntradayVwapsRequest']
_INTRADAYVWAPSRESPONSE = DESCRIPTOR.message_types_by_name['IntradayVwapsResponse']
_INTRADAYVWAP = DESCRIPTOR.message_types_by_name['IntradayVwap']
IntradayVwapsRequest = _reflection.GeneratedProtocolMessageType('IntradayVwapsRequest', (_message.Message,), {
  'DESCRIPTOR' : _INTRADAYVWAPSREQUEST,
  '__module__' : 'systemathics.apis.services.intraday.v1.intraday_vwap_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.intraday.v1.IntradayVwapsRequest)
  })
_sym_db.RegisterMessage(IntradayVwapsRequest)

IntradayVwapsResponse = _reflection.GeneratedProtocolMessageType('IntradayVwapsResponse', (_message.Message,), {
  'DESCRIPTOR' : _INTRADAYVWAPSRESPONSE,
  '__module__' : 'systemathics.apis.services.intraday.v1.intraday_vwap_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.intraday.v1.IntradayVwapsResponse)
  })
_sym_db.RegisterMessage(IntradayVwapsResponse)

IntradayVwap = _reflection.GeneratedProtocolMessageType('IntradayVwap', (_message.Message,), {
  'DESCRIPTOR' : _INTRADAYVWAP,
  '__module__' : 'systemathics.apis.services.intraday.v1.intraday_vwap_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.intraday.v1.IntradayVwap)
  })
_sym_db.RegisterMessage(IntradayVwap)

_INTRADAYVWAPSSERVICE = DESCRIPTOR.services_by_name['IntradayVwapsService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _INTRADAYVWAPSREQUEST._serialized_start=288
  _INTRADAYVWAPSREQUEST._serialized_end=526
  _INTRADAYVWAPSRESPONSE._serialized_start=528
  _INTRADAYVWAPSRESPONSE._serialized_end=619
  _INTRADAYVWAP._serialized_start=621
  _INTRADAYVWAP._serialized_end=729
  _INTRADAYVWAPSSERVICE._serialized_start=732
  _INTRADAYVWAPSSERVICE._serialized_end=897
# @@protoc_insertion_point(module_scope)
