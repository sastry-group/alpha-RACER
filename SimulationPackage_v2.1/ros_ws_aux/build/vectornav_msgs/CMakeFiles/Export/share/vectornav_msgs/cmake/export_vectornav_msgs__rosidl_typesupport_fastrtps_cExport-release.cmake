#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "vectornav_msgs::vectornav_msgs__rosidl_typesupport_fastrtps_c" for configuration "Release"
set_property(TARGET vectornav_msgs::vectornav_msgs__rosidl_typesupport_fastrtps_c APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(vectornav_msgs::vectornav_msgs__rosidl_typesupport_fastrtps_c PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libvectornav_msgs__rosidl_typesupport_fastrtps_c.so"
  IMPORTED_SONAME_RELEASE "libvectornav_msgs__rosidl_typesupport_fastrtps_c.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS vectornav_msgs::vectornav_msgs__rosidl_typesupport_fastrtps_c )
list(APPEND _IMPORT_CHECK_FILES_FOR_vectornav_msgs::vectornav_msgs__rosidl_typesupport_fastrtps_c "${_IMPORT_PREFIX}/lib/libvectornav_msgs__rosidl_typesupport_fastrtps_c.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
