// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/protobuf/tpu/dynamic_padding.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fprotobuf_2ftpu_2fdynamic_5fpadding_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fprotobuf_2ftpu_2fdynamic_5fpadding_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3009000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3009002 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_table_driven.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/inlined_string_field.h>
#include <google/protobuf/metadata.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcore_2fprotobuf_2ftpu_2fdynamic_5fpadding_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tensorflow_2fcore_2fprotobuf_2ftpu_2fdynamic_5fpadding_2eproto {
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTableField entries[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::AuxillaryParseTableField aux[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTable schema[1]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::FieldMetadata field_metadata[];
  static const ::PROTOBUF_NAMESPACE_ID::internal::SerializationTable serialization_table[];
  static const ::PROTOBUF_NAMESPACE_ID::uint32 offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcore_2fprotobuf_2ftpu_2fdynamic_5fpadding_2eproto;
namespace tensorflow {
namespace tpu {
class PaddingMap;
class PaddingMapDefaultTypeInternal;
extern PaddingMapDefaultTypeInternal _PaddingMap_default_instance_;
}  // namespace tpu
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> ::tensorflow::tpu::PaddingMap* Arena::CreateMaybeMessage<::tensorflow::tpu::PaddingMap>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {
namespace tpu {

// ===================================================================

class PaddingMap :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.tpu.PaddingMap) */ {
 public:
  PaddingMap();
  virtual ~PaddingMap();

  PaddingMap(const PaddingMap& from);
  PaddingMap(PaddingMap&& from) noexcept
    : PaddingMap() {
    *this = ::std::move(from);
  }

  inline PaddingMap& operator=(const PaddingMap& from) {
    CopyFrom(from);
    return *this;
  }
  inline PaddingMap& operator=(PaddingMap&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  inline ::PROTOBUF_NAMESPACE_ID::Arena* GetArena() const final {
    return GetArenaNoVirtual();
  }
  inline void* GetMaybeArenaPointer() const final {
    return MaybeArenaPtr();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return GetMetadataStatic().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return GetMetadataStatic().reflection;
  }
  static const PaddingMap& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const PaddingMap* internal_default_instance() {
    return reinterpret_cast<const PaddingMap*>(
               &_PaddingMap_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(PaddingMap& a, PaddingMap& b) {
    a.Swap(&b);
  }
  inline void Swap(PaddingMap* other) {
    if (other == this) return;
    if (GetArenaNoVirtual() == other->GetArenaNoVirtual()) {
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(PaddingMap* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetArenaNoVirtual() == other->GetArenaNoVirtual());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  inline PaddingMap* New() const final {
    return CreateMaybeMessage<PaddingMap>(nullptr);
  }

  PaddingMap* New(::PROTOBUF_NAMESPACE_ID::Arena* arena) const final {
    return CreateMaybeMessage<PaddingMap>(arena);
  }
  void CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void CopyFrom(const PaddingMap& from);
  void MergeFrom(const PaddingMap& from);
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  #if GOOGLE_PROTOBUF_ENABLE_EXPERIMENTAL_PARSER
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  #else
  bool MergePartialFromCodedStream(
      ::PROTOBUF_NAMESPACE_ID::io::CodedInputStream* input) final;
  #endif  // GOOGLE_PROTOBUF_ENABLE_EXPERIMENTAL_PARSER
  void SerializeWithCachedSizes(
      ::PROTOBUF_NAMESPACE_ID::io::CodedOutputStream* output) const final;
  ::PROTOBUF_NAMESPACE_ID::uint8* InternalSerializeWithCachedSizesToArray(
      ::PROTOBUF_NAMESPACE_ID::uint8* target) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  inline void SharedCtor();
  inline void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(PaddingMap* other);
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.tpu.PaddingMap";
  }
  protected:
  explicit PaddingMap(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  private:
  static void ArenaDtor(void* object);
  inline void RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  private:
  inline ::PROTOBUF_NAMESPACE_ID::Arena* GetArenaNoVirtual() const {
    return _internal_metadata_.arena();
  }
  inline void* MaybeArenaPtr() const {
    return _internal_metadata_.raw_arena_ptr();
  }
  public:

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;
  private:
  static ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadataStatic() {
    ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&::descriptor_table_tensorflow_2fcore_2fprotobuf_2ftpu_2fdynamic_5fpadding_2eproto);
    return ::descriptor_table_tensorflow_2fcore_2fprotobuf_2ftpu_2fdynamic_5fpadding_2eproto.file_level_metadata[kIndexInFileMessages];
  }

  public:

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kArgIndexFieldNumber = 1,
    kShapeIndexFieldNumber = 2,
    kPaddingArgIndexFieldNumber = 3,
  };
  // int32 arg_index = 1;
  void clear_arg_index();
  ::PROTOBUF_NAMESPACE_ID::int32 arg_index() const;
  void set_arg_index(::PROTOBUF_NAMESPACE_ID::int32 value);

  // int32 shape_index = 2;
  void clear_shape_index();
  ::PROTOBUF_NAMESPACE_ID::int32 shape_index() const;
  void set_shape_index(::PROTOBUF_NAMESPACE_ID::int32 value);

  // int32 padding_arg_index = 3;
  void clear_padding_arg_index();
  ::PROTOBUF_NAMESPACE_ID::int32 padding_arg_index() const;
  void set_padding_arg_index(::PROTOBUF_NAMESPACE_ID::int32 value);

  // @@protoc_insertion_point(class_scope:tensorflow.tpu.PaddingMap)
 private:
  class _Internal;

  ::PROTOBUF_NAMESPACE_ID::internal::InternalMetadataWithArena _internal_metadata_;
  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  ::PROTOBUF_NAMESPACE_ID::int32 arg_index_;
  ::PROTOBUF_NAMESPACE_ID::int32 shape_index_;
  ::PROTOBUF_NAMESPACE_ID::int32 padding_arg_index_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_tensorflow_2fcore_2fprotobuf_2ftpu_2fdynamic_5fpadding_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// PaddingMap

// int32 arg_index = 1;
inline void PaddingMap::clear_arg_index() {
  arg_index_ = 0;
}
inline ::PROTOBUF_NAMESPACE_ID::int32 PaddingMap::arg_index() const {
  // @@protoc_insertion_point(field_get:tensorflow.tpu.PaddingMap.arg_index)
  return arg_index_;
}
inline void PaddingMap::set_arg_index(::PROTOBUF_NAMESPACE_ID::int32 value) {
  
  arg_index_ = value;
  // @@protoc_insertion_point(field_set:tensorflow.tpu.PaddingMap.arg_index)
}

// int32 shape_index = 2;
inline void PaddingMap::clear_shape_index() {
  shape_index_ = 0;
}
inline ::PROTOBUF_NAMESPACE_ID::int32 PaddingMap::shape_index() const {
  // @@protoc_insertion_point(field_get:tensorflow.tpu.PaddingMap.shape_index)
  return shape_index_;
}
inline void PaddingMap::set_shape_index(::PROTOBUF_NAMESPACE_ID::int32 value) {
  
  shape_index_ = value;
  // @@protoc_insertion_point(field_set:tensorflow.tpu.PaddingMap.shape_index)
}

// int32 padding_arg_index = 3;
inline void PaddingMap::clear_padding_arg_index() {
  padding_arg_index_ = 0;
}
inline ::PROTOBUF_NAMESPACE_ID::int32 PaddingMap::padding_arg_index() const {
  // @@protoc_insertion_point(field_get:tensorflow.tpu.PaddingMap.padding_arg_index)
  return padding_arg_index_;
}
inline void PaddingMap::set_padding_arg_index(::PROTOBUF_NAMESPACE_ID::int32 value) {
  
  padding_arg_index_ = value;
  // @@protoc_insertion_point(field_set:tensorflow.tpu.PaddingMap.padding_arg_index)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace tpu
}  // namespace tensorflow

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fprotobuf_2ftpu_2fdynamic_5fpadding_2eproto
