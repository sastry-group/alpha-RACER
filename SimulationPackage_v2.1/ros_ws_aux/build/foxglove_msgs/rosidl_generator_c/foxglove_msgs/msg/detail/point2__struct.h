// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from foxglove_msgs:msg/Point2.idl
// generated code does not contain a copyright notice

#ifndef FOXGLOVE_MSGS__MSG__DETAIL__POINT2__STRUCT_H_
#define FOXGLOVE_MSGS__MSG__DETAIL__POINT2__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Point2 in the package foxglove_msgs.
/**
  * foxglove_msgs/msg/Point2
  * A point representing a position in 2D space
 */
typedef struct foxglove_msgs__msg__Point2
{
  /// Generated by https://github.com/foxglove/schemas
  /// x coordinate position
  double x;
  /// y coordinate position
  double y;
} foxglove_msgs__msg__Point2;

// Struct for a sequence of foxglove_msgs__msg__Point2.
typedef struct foxglove_msgs__msg__Point2__Sequence
{
  foxglove_msgs__msg__Point2 * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} foxglove_msgs__msg__Point2__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // FOXGLOVE_MSGS__MSG__DETAIL__POINT2__STRUCT_H_
