# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorTransfer.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorTransfer.proto',
  package='tensorTransfer',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x14tensorTransfer.proto\x12\x0etensorTransfer\"&\n\x07Request\x12\r\n\x05shape\x18\x01 \x03(\x03\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\"\x1a\n\x07Reponse\x12\x0f\n\x07message\x18\x01 \x01(\t2R\n\x0etensorTransfer\x12@\n\x0cSimpleMethod\x12\x17.tensorTransfer.Request\x1a\x17.tensorTransfer.Reponseb\x06proto3'
)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='tensorTransfer.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='shape', full_name='tensorTransfer.Request.shape', index=0,
      number=1, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='tensorTransfer.Request.data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
  serialized_start=40,
  serialized_end=78,
)


_REPONSE = _descriptor.Descriptor(
  name='Reponse',
  full_name='tensorTransfer.Reponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='tensorTransfer.Reponse.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=80,
  serialized_end=106,
)

DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Reponse'] = _REPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
  'DESCRIPTOR' : _REQUEST,
  '__module__' : 'tensorTransfer_pb2'
  # @@protoc_insertion_point(class_scope:tensorTransfer.Request)
  })
_sym_db.RegisterMessage(Request)

Reponse = _reflection.GeneratedProtocolMessageType('Reponse', (_message.Message,), {
  'DESCRIPTOR' : _REPONSE,
  '__module__' : 'tensorTransfer_pb2'
  # @@protoc_insertion_point(class_scope:tensorTransfer.Reponse)
  })
_sym_db.RegisterMessage(Reponse)



_TENSORTRANSFER = _descriptor.ServiceDescriptor(
  name='tensorTransfer',
  full_name='tensorTransfer.tensorTransfer',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=108,
  serialized_end=190,
  methods=[
  _descriptor.MethodDescriptor(
    name='SimpleMethod',
    full_name='tensorTransfer.tensorTransfer.SimpleMethod',
    index=0,
    containing_service=None,
    input_type=_REQUEST,
    output_type=_REPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TENSORTRANSFER)

DESCRIPTOR.services_by_name['tensorTransfer'] = _TENSORTRANSFER

# @@protoc_insertion_point(module_scope)