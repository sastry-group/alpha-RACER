# generated from rosidl_generator_py/resource/_idl.py.em
# with input from novatel_oem7_msgs:srv/Oem7AbasciiCmd.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Oem7AbasciiCmd_Request(type):
    """Metaclass of message 'Oem7AbasciiCmd_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
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
                'novatel_oem7_msgs.srv.Oem7AbasciiCmd_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__oem7_abascii_cmd__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__oem7_abascii_cmd__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__oem7_abascii_cmd__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__oem7_abascii_cmd__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__oem7_abascii_cmd__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Oem7AbasciiCmd_Request(metaclass=Metaclass_Oem7AbasciiCmd_Request):
    """Message class 'Oem7AbasciiCmd_Request'."""

    __slots__ = [
        '_cmd',
    ]

    _fields_and_field_types = {
        'cmd': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.cmd = kwargs.get('cmd', str())

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
        if self.cmd != other.cmd:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def cmd(self):
        """Message field 'cmd'."""
        return self._cmd

    @cmd.setter
    def cmd(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'cmd' field must be of type 'str'"
        self._cmd = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_Oem7AbasciiCmd_Response(type):
    """Metaclass of message 'Oem7AbasciiCmd_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
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
                'novatel_oem7_msgs.srv.Oem7AbasciiCmd_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__oem7_abascii_cmd__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__oem7_abascii_cmd__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__oem7_abascii_cmd__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__oem7_abascii_cmd__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__oem7_abascii_cmd__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Oem7AbasciiCmd_Response(metaclass=Metaclass_Oem7AbasciiCmd_Response):
    """Message class 'Oem7AbasciiCmd_Response'."""

    __slots__ = [
        '_rsp',
    ]

    _fields_and_field_types = {
        'rsp': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.rsp = kwargs.get('rsp', str())

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
        if self.rsp != other.rsp:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def rsp(self):
        """Message field 'rsp'."""
        return self._rsp

    @rsp.setter
    def rsp(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'rsp' field must be of type 'str'"
        self._rsp = value


class Metaclass_Oem7AbasciiCmd(type):
    """Metaclass of service 'Oem7AbasciiCmd'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('novatel_oem7_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'novatel_oem7_msgs.srv.Oem7AbasciiCmd')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__oem7_abascii_cmd

            from novatel_oem7_msgs.srv import _oem7_abascii_cmd
            if _oem7_abascii_cmd.Metaclass_Oem7AbasciiCmd_Request._TYPE_SUPPORT is None:
                _oem7_abascii_cmd.Metaclass_Oem7AbasciiCmd_Request.__import_type_support__()
            if _oem7_abascii_cmd.Metaclass_Oem7AbasciiCmd_Response._TYPE_SUPPORT is None:
                _oem7_abascii_cmd.Metaclass_Oem7AbasciiCmd_Response.__import_type_support__()


class Oem7AbasciiCmd(metaclass=Metaclass_Oem7AbasciiCmd):
    from novatel_oem7_msgs.srv._oem7_abascii_cmd import Oem7AbasciiCmd_Request as Request
    from novatel_oem7_msgs.srv._oem7_abascii_cmd import Oem7AbasciiCmd_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
