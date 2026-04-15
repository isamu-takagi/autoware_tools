cmake_minimum_required(VERSION 3.14)
project(autoware_adapi_testing)

find_package(autoware_cmake REQUIRED)
autoware_package()
ament_python_install_package(${PROJECT_NAME} PACKAGE_DIR src)
install(PROGRAMS script/autoware_adapi_testing DESTINATION lib/${PROJECT_NAME})
ament_auto_package(INSTALL_TO_SHARE script test)
