# generated from rosidl_generator_py/resource/_idl.py.em
# with input from novatel_oem7_msgs:msg/INSReceiverStatus.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

# Member 'status'
import numpy  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_INSReceiverStatus(type):
    """Metaclass of message 'INSReceiverStatus'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'INS_RESET_BYTE': 0,
        'BYTE_1': 1,
        'IMU_COMMUNICATION_ERROR': 1,
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('novatel_oem7_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'novatel_oem7_msgs.msg.INSReceiverStatus')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__ins_receiver_status
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__ins_receiver_status
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__ins_receiver_status
            cls._TYPE_SUPPORT = module.type_support_msg__msg__ins_receiver_status
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__ins_receiver_status

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'INS_RESET_BYTE': cls.__constants['INS_RESET_BYTE'],
            'BYTE_1': cls.__constants['BYTE_1'],
            'IMU_COMMUNICATION_ERROR': cls.__constants['IMU_COMMUNICATION_ERROR'],
        }

    @property
    def INS_RESET_BYTE(self):
        """Message constant 'INS_RESET_BYTE'."""
        return Metaclass_INSReceiverStatus.__constants['INS_RESET_BYTE']

    @property
    def BYTE_1(self):
        """Message constant 'BYTE_1'."""
        return Metaclass_INSReceiverStatus.__constants['BYTE_1']

    @property
    def IMU_COMMUNICATION_ERROR(self):
        """Message constant 'IMU_COMMUNICATION_ERROR'."""
        return Metaclass_INSReceiverStatus.__constants['IMU_COMMUNICATION_ERROR']


class INSReceiverStatus(metaclass=Metaclass_INSReceiverStatus):
    """
    Message class 'INSReceiverStatus'.

    Constants:
      INS_RESET_BYTE
      BYTE_1
      IMU_COMMUNICATION_ERROR
    """

    __slots__ = [
        '_status',
    ]

    _fields_and_field_types = {
        'status': 'uint8[4]',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('uint8'), 4),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        if 'status' not in kwargs:
            self.status = numpy.zeros(4, dtype=numpy.uint8)
        else:
            self.status = numpy.array(kwargs.get('status'), dtype=numpy.uint8)
            assert self.status.shape == (4, )

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if all(self.status != other.status):
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def status(self):
        """Message field 'status'."""
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, numpy.ndarray):
            assert value.dtype == numpy.uint8, \
                "The 'status' numpy.ndarray() must have the dtype of 'numpy.uint8'"
            assert value.size == 4, \
                "The 'status' numpy.ndarray() must have a size of 4"
            self._status = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 4 and
                 all(isinstance(v, int) for v in value) and
                 all(val >= 0 and val < 256 for val in value)), \
                "The 'status' field must be a set or sequence with length 4 and each value of type 'int' and each unsigned integer in [0, 255]"
        self._status = numpy.array(value, dtype=numpy.uint8)
