cmake_minimum_required(VERSION 2.8.3)
project(lidar_control)

find_package(PCL REQUIRED)
find_package(catkin REQUIRED COMPONENTS
  roscpp
  sensor_msgs
  pcl_ros
)

include_directories(
  ${catkin_INCLUDE_DIRS}
  ${PCL_INCLUDE_DIRS}
)

catkin_package()

add_executable(lidar_control src/main.cpp)
target_link_libraries(lidar_control ${catkin_LIBRARIES} ${PCL_LIBRARIES})

