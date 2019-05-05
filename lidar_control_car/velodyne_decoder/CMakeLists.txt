cmake_minimum_required(VERSION 2.8.3)
project(velodyne_decoder)

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

add_executable(velodyne_decoder src/main.cpp)
target_link_libraries(velodyne_decoder ${catkin_LIBRARIES} ${PCL_LIBRARIES})

