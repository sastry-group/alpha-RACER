// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from raptor_dbw_msgs:msg/Brake2Report.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "raptor_dbw_msgs/msg/detail/brake2_report__struct.h"
#include "raptor_dbw_msgs/msg/detail/brake2_report__functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool raptor_dbw_msgs__msg__brake2_report__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[48];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("raptor_dbw_msgs.msg._brake2_report.Brake2Report", full_classname_dest, 47) == 0);
  }
  raptor_dbw_msgs__msg__Brake2Report * ros_message = _ros_message;
  {  // header
    PyObject * field = PyObject_GetAttrString(_pymsg, "header");
    if (!field) {
      return false;
    }
    if (!std_msgs__msg__header__convert_from_py(field, &ros_message->header)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // front_brake_pressure
    PyObject * field = PyObject_GetAttrString(_pymsg, "front_brake_pressure");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->front_brake_pressure = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // rear_brake_pressure
    PyObject * field = PyObject_GetAttrString(_pymsg, "rear_brake_pressure");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->rear_brake_pressure = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // rolling_counter
    PyObject * field = PyObject_GetAttrString(_pymsg, "rolling_counter");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->rolling_counter = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // estimated_road_slope
    PyObject * field = PyObject_GetAttrString(_pymsg, "estimated_road_slope");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->estimated_road_slope = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // speed_set_point
    PyObject * field = PyObject_GetAttrString(_pymsg, "speed_set_point");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->speed_set_point = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * raptor_dbw_msgs__msg__brake2_report__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of Brake2Report */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("raptor_dbw_msgs.msg._brake2_report");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "Brake2Report");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  raptor_dbw_msgs__msg__Brake2Report * ros_message = (raptor_dbw_msgs__msg__Brake2Report *)raw_ros_message;
  {  // header
    PyObject * field = NULL;
    field = std_msgs__msg__header__convert_to_py(&ros_message->header);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "header", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // front_brake_pressure
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->front_brake_pressure);
    {
      int rc = PyObject_SetAttrString(_pymessage, "front_brake_pressure", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // rear_brake_pressure
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->rear_brake_pressure);
    {
      int rc = PyObject_SetAttrString(_pymessage, "rear_brake_pressure", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // rolling_counter
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->rolling_counter);
    {
      int rc = PyObject_SetAttrString(_pymessage, "rolling_counter", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // estimated_road_slope
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->estimated_road_slope);
    {
      int rc = PyObject_SetAttrString(_pymessage, "estimated_road_slope", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // speed_set_point
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->speed_set_point);
    {
      int rc = PyObject_SetAttrString(_pymessage, "speed_set_point", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
