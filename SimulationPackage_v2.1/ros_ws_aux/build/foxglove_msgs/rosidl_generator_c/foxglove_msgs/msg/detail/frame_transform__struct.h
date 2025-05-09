// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from foxglove_msgs:msg/FrameTransform.idl
// generated code does not contain a copyright notice

#ifndef FOXGLOVE_MSGS__MSG__DETAIL__FRAME_TRANSFORM__STRUCT_H_
#define FOXGLOVE_MSGS__MSG__DETAIL__FRAME_TRANSFORM__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__struct.h"
// Member 'parent_frame_id'
// Member 'child_frame_id'
#include "rosidl_runtime_c/string.h"
// Member 'translation'
#include "geometry_msgs/msg/detail/vector3__struct.h"
// Member 'rotation'
#include "geometry_msgs/msg/detail/quaternion__struct.h"

/// Struct defined in msg/FrameTransform in the package foxglove_msgs.
/**
  * foxglove_msgs/msg/FrameTransform
  * A transform between two reference frames in 3D space
 */
typedef struct foxglove_msgs__msg__FrameTransform
{
  /// Generated by https://github.com/foxglove/schemas
  /// Timestamp of transform
  builtin_interfaces__msg__Time timestamp;
  /// Name of the parent frame
  rosidl_runtime_c__String parent_frame_id;
  /// Name of the child frame
  rosidl_runtime_c__String child_frame_id;
  /// Translation component of the transform
  geometry_msgs__msg__Vector3 translation;
  /// Rotation component of the transform
  geometry_msgs__msg__Quaternion rotation;
} foxglove_msgs__msg__FrameTransform;

// Struct for a sequence of foxglove_msgs__msg__FrameTransform.
typedef struct foxglove_msgs__msg__FrameTransform__Sequence
{
  foxglove_msgs__msg__FrameTransform * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} foxglove_msgs__msg__FrameTransform__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // FOXGLOVE_MSGS__MSG__DETAIL__FRAME_TRANSFORM__STRUCT_H_
