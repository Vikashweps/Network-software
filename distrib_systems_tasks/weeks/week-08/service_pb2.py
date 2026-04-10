
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    1,
    '',
    'service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rservice.proto\x12\x08likes.v1\"F\n\x04Like\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0e\n\x06\x61uthor\x18\x02 \x01(\t\x12\x0e\n\x06target\x18\x03 \x01(\t\x12\x12\n\ncreated_at\x18\x04 \x01(\x03\"3\n\x11\x43reateLikeRequest\x12\x0e\n\x06\x61uthor\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\"\x1c\n\x0eGetLikeRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"\x12\n\x10ListLikesRequest\"2\n\x11ListLikesResponse\x12\x1d\n\x05likes\x18\x01 \x03(\x0b\x32\x0e.likes.v1.Like\":\n\x12StreamLikesRequest\x12\x15\n\rtarget_filter\x18\x01 \x01(\t\x12\r\n\x05\x63ount\x18\x02 \x01(\x05\x32\x83\x02\n\x0cLikesService\x12\x39\n\nCreateLike\x12\x1b.likes.v1.CreateLikeRequest\x1a\x0e.likes.v1.Like\x12\x33\n\x07GetLike\x12\x18.likes.v1.GetLikeRequest\x1a\x0e.likes.v1.Like\x12\x44\n\tListLikes\x12\x1a.likes.v1.ListLikesRequest\x1a\x1b.likes.v1.ListLikesResponse\x12=\n\x0bStreamLikes\x12\x1c.likes.v1.StreamLikesRequest\x1a\x0e.likes.v1.Like0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_LIKE']._serialized_start=27
  _globals['_LIKE']._serialized_end=97
  _globals['_CREATELIKEREQUEST']._serialized_start=99
  _globals['_CREATELIKEREQUEST']._serialized_end=150
  _globals['_GETLIKEREQUEST']._serialized_start=152
  _globals['_GETLIKEREQUEST']._serialized_end=180
  _globals['_LISTLIKESREQUEST']._serialized_start=182
  _globals['_LISTLIKESREQUEST']._serialized_end=200
  _globals['_LISTLIKESRESPONSE']._serialized_start=202
  _globals['_LISTLIKESRESPONSE']._serialized_end=252
  _globals['_STREAMLIKESREQUEST']._serialized_start=254
  _globals['_STREAMLIKESREQUEST']._serialized_end=312
  _globals['_LIKESSERVICE']._serialized_start=315
  _globals['_LIKESSERVICE']._serialized_end=574
# @@protoc_insertion_point(module_scope)
