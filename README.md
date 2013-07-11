Navigation Test
===============

## Todo

#### High Priority
- Include video and map topics into bag file
- ~~Distinguish between navigation component results (aborted and other)~~
- ~~Distinguish between failure and error in rostset~~
- Move generic launchfile settings into seperate yaml file. 
  Eventually only the four arguments robot, navigation, scenario_name, yaml_config are passed to navigation_test_skeleton
- Fix application developer view in component_catalogue
- Enhance bag_recorder to ignore non-published topics

##### Mid Priority
- Update component catalogue filter to display the last x results globally ( not for each series )
- In case of an error, display the actual metrics of the test ( distance, duration, rotation )
- Make navigation_test_analysis a daemon waiting for new bag files
- Adjustable video frequency
- Record video file in navigation_test_analysis and upload to seperate fileserver
- Create navigation_test_video_publisher that serves as a gateway between fileserver and webserver
- Include ros dependency for avconv in github.org/ros/rosdistro
- Sometimes a collision is detected on initial simulation startup due to the robot falling on the ground
