Navigation Test
===============

## Todo

#### High Priority
- Include ~~video and~~ map topics into bag file
- Start / Stop Service for bagrecorder and collision detection

##### Mid Priority
- Adjustable video frequency
- Include ros dependency for avconv in github.org/ros/rosdistro
- Sometimes a collision is detected on initial simulation startup due to the robot falling on the ground
- Highlight error messages thrown during startup (e.g. bagPath not writable)
- ~~Update Start- / Enddate in search to include all Test within the corresponding time window. I.e. start: dd/mm/yyyy 00:00, end: dd/mm/yyyy 23:59:59~~

#### Implemented
- ~~Create navigation_test_video_publisher that serves as a gateway between fileserver and webserver~~
- ~~Distinguish between navigation component results (aborted and other)~~
- ~~Distinguish between failure and error in rostset~~
- ~~Fix application developer view in component_catalogue~~
- ~~Enhance bag_recorder to ignore non-published topics~~
- ~~Update component catalogue filter to display the last x results globally ( not for each series )~~
- ~~Make navigation_test_analysis a daemon waiting for new bag files~~
- ~~Record video file in navigation_test_analysis and upload to seperate fileserver~~
- ~~move_base_action set in yaml config~~
- ~~Move generic launchfile settings into seperate yaml file.
  Eventually only the four arguments exclude cob specific parameter, robot, navigation, scenario_name, yaml_config are passed to navigation_test_skeleton~~
- ~~Include Parameter to dynamically configure recorded camera topics~~
- ~~Pass array of bumper topics to navigation_test_collisions~~
- ~~In case of an error, display the actual metrics of the test ( distance, duration, rotation )~~
