// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from foxglove_msgs:msg/PosesInFrame.idl
// generated code does not contain a copyright notice

#ifndef FOXGLOVE_MSGS__MSG__DETAIL__POSES_IN_FRAME__STRUCT_H_
#define FOXGLOVE_MSGS__MSG__DETAIL__POSES_IN_FRAME__STRUCT_H_

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
// Member 'frame_id'
#include "rosidl_runtime_c/string.h"
// Member 'poses'
#include "geometry_msgs/msg/detail/pose__struct.h"

/// Struct defined in msg/PosesInFrame in the package foxglove_msgs.
/**
  * foxglove_msgs/msg/PosesInFrame
  * An array of timestamped poses for an object or reference frame in 3D space
 */
typedef struct foxglove_msgs__msg__PosesInFrame
{
  /// Generated by https://github.com/foxglove/schemas
  /// Timestamp of pose
  builtin_interfaces__msg__Time timestamp;
  /// Frame of reference for pose position and orientation
  rosidl_runtime_c__String frame_id;
  /// Poses in 3D space
  geometry_msgs__msg__Pose__Sequence poses;
} foxglove_msgs__msg__PosesInFrame;

// Struct for a sequence of foxglove_msgs__msg__PosesInFrame.
typedef struct foxglove_msgs__msg__PosesInFrame__Sequence
{
  foxglove_msgs__msg__PosesInFrame * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} foxglove_msgs__msg__PosesInFrame__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // FOXGLOVE_MSGS__MSG__DETAIL__POSES_IN_FRAME__STRUCT_H_
