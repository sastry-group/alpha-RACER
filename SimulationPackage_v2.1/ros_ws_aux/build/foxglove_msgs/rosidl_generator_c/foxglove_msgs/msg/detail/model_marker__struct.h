// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from foxglove_msgs:msg/ModelMarker.idl
// generated code does not contain a copyright notice

#ifndef FOXGLOVE_MSGS__MSG__DETAIL__MODEL_MARKER__STRUCT_H_
#define FOXGLOVE_MSGS__MSG__DETAIL__MODEL_MARKER__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'scale'
#include "geometry_msgs/msg/detail/vector3__struct.h"
// Member 'color'
#include "foxglove_msgs/msg/detail/color__struct.h"
// Member 'url'
// Member 'mime_type'
#include "rosidl_runtime_c/string.h"
// Member 'data'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/ModelMarker in the package foxglove_msgs.
/**
  * foxglove_msgs/msg/ModelMarker
  * A marker representing a 3D model
 */
typedef struct foxglove_msgs__msg__ModelMarker
{
  /// Generated by https://github.com/foxglove/schemas
  /// Origin of model relative to reference frame
  geometry_msgs__msg__Pose pose;
  /// Scale factor to apply to the model along each axis
  geometry_msgs__msg__Vector3 scale;
  /// Solid color to use for the whole model. If `use_embedded_materials` is true, this color is blended on top of the embedded material color.
  foxglove_msgs__msg__Color color;
  /// Whether to use materials embedded in the model, or only the `color`
  bool use_embedded_materials;
  /// URL pointing to model file. Either `url` or `mime_type` and `data` should be provided.
  rosidl_runtime_c__String url;
  /// MIME type of embedded model (e.g. `model/gltf-binary`). Either `url` or `mime_type` and `data` should be provided.
  rosidl_runtime_c__String mime_type;
  /// Embedded model. Either `url` or `mime_type` and `data` should be provided.
  rosidl_runtime_c__uint8__Sequence data;
} foxglove_msgs__msg__ModelMarker;

// Struct for a sequence of foxglove_msgs__msg__ModelMarker.
typedef struct foxglove_msgs__msg__ModelMarker__Sequence
{
  foxglove_msgs__msg__ModelMarker * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} foxglove_msgs__msg__ModelMarker__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // FOXGLOVE_MSGS__MSG__DETAIL__MODEL_MARKER__STRUCT_H_
