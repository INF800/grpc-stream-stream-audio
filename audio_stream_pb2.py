# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: audio_stream.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x61udio_stream.proto\x12\x0c\x61udio_stream\"\x1a\n\nAudioChunk\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\" \n\rAudioResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2^\n\x12\x41udioStreamService\x12H\n\x0bStreamAudio\x12\x18.audio_stream.AudioChunk\x1a\x1b.audio_stream.AudioResponse(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'audio_stream_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_AUDIOCHUNK']._serialized_start=36
  _globals['_AUDIOCHUNK']._serialized_end=62
  _globals['_AUDIORESPONSE']._serialized_start=64
  _globals['_AUDIORESPONSE']._serialized_end=96
  _globals['_AUDIOSTREAMSERVICE']._serialized_start=98
  _globals['_AUDIOSTREAMSERVICE']._serialized_end=192
# @@protoc_insertion_point(module_scope)
