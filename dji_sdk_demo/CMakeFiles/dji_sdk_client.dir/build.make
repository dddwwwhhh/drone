# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/dronepi2/Desktop/Onboard-SDK-ROS

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/dronepi2/Desktop/Onboard-SDK-ROS

# Include any dependencies generated for this target.
include dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/depend.make

# Include the progress variables for this target.
include dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/progress.make

# Include the compile flags for this target's objects.
include dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/flags.make

dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/src/client.cpp.o: dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/flags.make
dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/src/client.cpp.o: dji_sdk_demo/src/client.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/dronepi2/Desktop/Onboard-SDK-ROS/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/src/client.cpp.o"
	cd /home/dronepi2/Desktop/Onboard-SDK-ROS/dji_sdk_demo && /usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/dji_sdk_client.dir/src/client.cpp.o -c /home/dronepi2/Desktop/Onboard-SDK-ROS/dji_sdk_demo/src/client.cpp

dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/src/client.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dji_sdk_client.dir/src/client.cpp.i"
	cd /home/dronepi2/Desktop/Onboard-SDK-ROS/dji_sdk_demo && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/dronepi2/Desktop/Onboard-SDK-ROS/dji_sdk_demo/src/client.cpp > CMakeFiles/dji_sdk_client.dir/src/client.cpp.i

dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/src/client.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dji_sdk_client.dir/src/client.cpp.s"
	cd /home/dronepi2/Desktop/Onboard-SDK-ROS/dji_sdk_demo && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/dronepi2/Desktop/Onboard-SDK-ROS/dji_sdk_demo/src/client.cpp -o CMakeFiles/dji_sdk_client.dir/src/client.cpp.s

dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/src/client.cpp.o.requires:

.PHONY : dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/src/client.cpp.o.requires

dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/src/client.cpp.o.provides: dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/src/client.cpp.o.requires
	$(MAKE) -f dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/build.make dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/src/client.cpp.o.provides.build
.PHONY : dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/src/client.cpp.o.provides

dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/src/client.cpp.o.provides.build: dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/src/client.cpp.o


# Object files for target dji_sdk_client
dji_sdk_client_OBJECTS = \
"CMakeFiles/dji_sdk_client.dir/src/client.cpp.o"

# External object files for target dji_sdk_client
dji_sdk_client_EXTERNAL_OBJECTS =

devel/lib/dji_sdk_demo/dji_sdk_client: dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/src/client.cpp.o
devel/lib/dji_sdk_demo/dji_sdk_client: dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/build.make
devel/lib/dji_sdk_demo/dji_sdk_client: /opt/ros/kinetic/lib/libactionlib.so
devel/lib/dji_sdk_demo/dji_sdk_client: /opt/ros/kinetic/lib/libroscpp.so
devel/lib/dji_sdk_demo/dji_sdk_client: /usr/lib/arm-linux-gnueabihf/libboost_signals.so
devel/lib/dji_sdk_demo/dji_sdk_client: /usr/lib/arm-linux-gnueabihf/libboost_filesystem.so
devel/lib/dji_sdk_demo/dji_sdk_client: /opt/ros/kinetic/lib/librosconsole.so
devel/lib/dji_sdk_demo/dji_sdk_client: /opt/ros/kinetic/lib/librosconsole_log4cxx.so
devel/lib/dji_sdk_demo/dji_sdk_client: /opt/ros/kinetic/lib/librosconsole_backend_interface.so
devel/lib/dji_sdk_demo/dji_sdk_client: /usr/lib/arm-linux-gnueabihf/liblog4cxx.so
devel/lib/dji_sdk_demo/dji_sdk_client: /usr/lib/arm-linux-gnueabihf/libboost_regex.so
devel/lib/dji_sdk_demo/dji_sdk_client: /opt/ros/kinetic/lib/libxmlrpcpp.so
devel/lib/dji_sdk_demo/dji_sdk_client: /opt/ros/kinetic/lib/libroscpp_serialization.so
devel/lib/dji_sdk_demo/dji_sdk_client: /opt/ros/kinetic/lib/librostime.so
devel/lib/dji_sdk_demo/dji_sdk_client: /opt/ros/kinetic/lib/libcpp_common.so
devel/lib/dji_sdk_demo/dji_sdk_client: /usr/lib/arm-linux-gnueabihf/libboost_system.so
devel/lib/dji_sdk_demo/dji_sdk_client: /usr/lib/arm-linux-gnueabihf/libboost_thread.so
devel/lib/dji_sdk_demo/dji_sdk_client: /usr/lib/arm-linux-gnueabihf/libboost_chrono.so
devel/lib/dji_sdk_demo/dji_sdk_client: /usr/lib/arm-linux-gnueabihf/libboost_date_time.so
devel/lib/dji_sdk_demo/dji_sdk_client: /usr/lib/arm-linux-gnueabihf/libboost_atomic.so
devel/lib/dji_sdk_demo/dji_sdk_client: /usr/lib/arm-linux-gnueabihf/libpthread.so
devel/lib/dji_sdk_demo/dji_sdk_client: /usr/lib/arm-linux-gnueabihf/libconsole_bridge.so
devel/lib/dji_sdk_demo/dji_sdk_client: devel/lib/libdji_sdk_lib.a
devel/lib/dji_sdk_demo/dji_sdk_client: dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/dronepi2/Desktop/Onboard-SDK-ROS/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../devel/lib/dji_sdk_demo/dji_sdk_client"
	cd /home/dronepi2/Desktop/Onboard-SDK-ROS/dji_sdk_demo && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/dji_sdk_client.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/build: devel/lib/dji_sdk_demo/dji_sdk_client

.PHONY : dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/build

dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/requires: dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/src/client.cpp.o.requires

.PHONY : dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/requires

dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/clean:
	cd /home/dronepi2/Desktop/Onboard-SDK-ROS/dji_sdk_demo && $(CMAKE_COMMAND) -P CMakeFiles/dji_sdk_client.dir/cmake_clean.cmake
.PHONY : dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/clean

dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/depend:
	cd /home/dronepi2/Desktop/Onboard-SDK-ROS && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/dronepi2/Desktop/Onboard-SDK-ROS /home/dronepi2/Desktop/Onboard-SDK-ROS/dji_sdk_demo /home/dronepi2/Desktop/Onboard-SDK-ROS /home/dronepi2/Desktop/Onboard-SDK-ROS/dji_sdk_demo /home/dronepi2/Desktop/Onboard-SDK-ROS/dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dji_sdk_demo/CMakeFiles/dji_sdk_client.dir/depend

