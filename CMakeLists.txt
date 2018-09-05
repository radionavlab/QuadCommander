cmake_minimum_required(VERSION 2.8.3)
project(QuadCommander)

find_package(catkin REQUIRED COMPONENTS
  rospy
  mg_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES ros_proxy_server
 CATKIN_DEPENDS rospy mg_msgs
#  DEPENDS system_lib
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
