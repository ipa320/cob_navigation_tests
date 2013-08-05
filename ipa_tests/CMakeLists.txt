cmake_minimum_required(VERSION 2.4.6)
include($ENV{ROS_ROOT}/core/rosbuild/rosbuild.cmake)

# Set the build type.  Options are:
#  Coverage       : w/ debug symbols, w/o optimization, w/ code-coverage
#  Debug          : w/ debug symbols, w/o optimization
#  Release        : w/o debug symbols, w/ optimization
#  RelWithDebInfo : w/ debug symbols, w/ optimization
#  MinSizeRel     : w/o debug symbols, w/ optimization, stripped binaries
#set(ROS_BUILD_TYPE RelWithDebInfo)

rosbuild_init()

#set the default path for built executables to the "bin" directory
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
#set the default path for built libraries to the "lib" directory
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

#uncomment if you have defined messages
#rosbuild_genmsg()
#uncomment if you have defined services
#rosbuild_gensrv()

### GENERATED ###

rosbuild_add_rostest(launch/generated/cob3-3_2dnav_ros_dwa_compact_route.launch  TIMEOUT 10000.0)
rosbuild_add_rostest(launch/generated/cob3-3_2dnav_ros_dwa_extended_route.launch  TIMEOUT 10000.0)
rosbuild_add_rostest(launch/generated/cob3-3_2dnav_ros_tr_compact_route.launch  TIMEOUT 10000.0)
rosbuild_add_rostest(launch/generated/cob3-3_2dnav_ros_tr_extended_route.launch  TIMEOUT 10000.0)
rosbuild_add_rostest(launch/generated/desire_2dnav_ros_dwa_compact_route.launch  TIMEOUT 10000.0)
rosbuild_add_rostest(launch/generated/desire_2dnav_ros_dwa_extended_route.launch  TIMEOUT 10000.0)
rosbuild_add_rostest(launch/generated/desire_2dnav_ros_tr_compact_route.launch  TIMEOUT 10000.0)
rosbuild_add_rostest(launch/generated/desire_2dnav_ros_tr_extended_route.launch  TIMEOUT 10000.0)
rosbuild_add_rostest(launch/generated/raw3-2_2dnav_ros_dwa_compact_route.launch  TIMEOUT 10000.0)
rosbuild_add_rostest(launch/generated/raw3-2_2dnav_ros_dwa_extended_route.launch  TIMEOUT 10000.0)
rosbuild_add_rostest(launch/generated/raw3-2_2dnav_ros_tr_compact_route.launch  TIMEOUT 10000.0)
rosbuild_add_rostest(launch/generated/raw3-2_2dnav_ros_tr_extended_route.launch  TIMEOUT 10000.0)
