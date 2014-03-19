# Run navigation tests
There is three ways to use the navigation tests: (i) simulation on your local machine (ii) tests on a real robot and (iii) simulation on a jenkins continuous integration server.

## Run simulation tests on your local machine

### Install dependencies
```
sudo apt-get install libavcodec-extra-53
```

### Checkout the code
Checkout https://github.com/ipa320/cob_navigation_tests into your ROS_PACKAGE_PATH, e.g. ```~/ros``` and build it.
```
mkdir -p ~/ros
git clone https://github.com/ipa320/cob_navigation_tests.git ~/ros/cob_navigation_tests
rosmake cob_navigation_tests navigation_test_samples
```

### Create your own test package
Create a new package with a dependency to navigation_test_skeleton, your simulation bringup package and your navigation package
```
cd ~/ros
roscreate-pkg my_navigation_test navigation_test_skeleton cob_bringup_sim cob_navigation_global
```
Add a launch and a config directory in your new package
```
roscd my_navigation_test
mkdir launch
mkdir config
```
Create a rostest file in the launch directory and fill it with [this example code](https://raw.github.com/ipa320/cob_navigation_tests/groovy_dev/navigation_test_samples/launch/sample_test_cob3-3_dwa.test)
```
gedit launch/my_test.test
```

and two configuration files, one for the robot (e.g. [cob3-3](https://raw.github.com/ipa320/cob_navigation_tests/groovy_dev/navigation_test_samples/config/prepare_robot_cob3-3.yaml))
```
gedit config/prepare_robot_cob3-3.yaml
```
and one for the scenario (e.g. [scene1](https://raw.github.com/ipa320/cob_navigation_tests/groovy_dev/navigation_test_samples/config/scene1.yaml))
```
gedit config/scene1.yaml
```

### Run the test
The result of the test will be either PASSED or FAILED and a bag file which can be used for furtehr analysis later on
```
mkdir ~/bagFiles
export BAGPATH=~/bagFiles
rostest my_navigation_test my_test.test
```
Depending on the speed of your machine, the selection of waypoints this will take some time. Please wait until gazebo shuts down automatically.
Now you should have a bag file in ```~/bagFiles```

## Run test on a real robot
tbd

## Run tests on a jenkins continuous integration server

### Preparation of your test package
Prepare your tests in a new test package as described in the section above and commit it to any github repository (as an example, we'll use https://github.com/ipa-fmw/cob_navigation_tests_fmw).
Add your ```my_test.test``` file with the ```rosbuild_add_rostest``` macro to the ```CMakeLists.txt``` file of your package so that the tests get executed by running ```make test``` in your package. Example:
```
rosbuild_check_for_display(disp)
if(disp)
  rosbuild_add_rostest(launch/my_test.test)
else(disp)
  rosbuild_add_roslaunch_check(launch robot:=cob3-3)
endif(disp)
```
Commit your changes and push it to github.
Note:
* The ```rosbuild_check_for_display``` checks if a graphical environment is available. We'll only run the simulation in a graphical environment.
* You can check your configuration manually by running ```make test``` in your test package.

### Configure your test pipeline on the jenkins server
Login to the jenkins server (we'll use http://cob-jenkins-server:8080, you can login with your ipa-apartment pool login).

Under "pipeline configuration" (http://cob-jenkins-server:8080/user/fmw/configure) you can configure your pipeline settings. 
* Press "add repository" and fill in the details for your test repository
* Press "more" and select "downstream build" and check the box for "Graphics Test"
* Press "add dependency" and fill in the details for the `cob_navigation_tests` repository which is
  * fork user: ipa320
  * repository: cob_navigation_tests
  * branch: groovy_dev
* Press another "add dependency" and fill in the details for the `cob_navigation` repository which is
  * fork user: ipa320
  * repository: cob_navigation
  * branch: groovy_dev
* If the validation of your input is good, press "generate pipeline"

### Start a build
A new build will be started automatically (after around 10min) and after every source code change.
You can also start a build manually with the "pipe_starter_manual" job by selecting your navigation test repository.

# Analyse test results
This step will analyse the data in the bag files generated above. We're using the following metrics
* Travelled distrance in m
* Amount of rotation in rad
* Time to reach target
* Amount of collisions (if ```bumperTopics``` topics are provided)
If an image topic was recorded we'll render a video.

All analysis can be do ne by starting (asuming all your bag files are copied to ```~/bagFiles```
```
mkdir ~/videoFiles
roslaunch navigation_test_analysis analyse_remaining_bag_files.launch bagPath:=~/bagFiles videoPath:=~/videoFiles keepalive:=False
```
Now your bag Files in ```~/bagFiles``` should all be renamed into ```*_analyzed``` and in a corresponding video files in ```~/videoFiles```.


Notes: 
* As the video is rendered from the current screen, please keep the image view window maximised on a single screen. There is no dual monitor setup supported yet.
* Make sure you have write permissions to the github repository listed in the ```scene1.yaml``` file (e.g. https://github.com/ipa320/cob_navigation_tests_results)

# Visualize component catalogue
```
roslaunch component_catalogue component_catalogue.launch
```

Now you can have a look at the results at [http://localhost:9000](http://localhost:9000).






# Open issues
Please report new issues at https://github.com/ipa320/cob_navigation_tests/issues.


#### High Priority
- Include ~~video and~~ map topics into bag file
- Start / Stop Service for bagrecorder and collision detection

##### Mid Priority
- Adjustable video frequency
- Include ros dependency for avconv in github.org/ros/rosdistro
- Sometimes a collision is detected on initial simulation startup due to the robot falling on the ground
- Highlight error messages thrown during startup (e.g. bagPath not writable)

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
- ~~Update Start- / Enddate in search to include all Test within the corresponding time window. I.e. start: dd/mm/yyyy 00:00, end: dd/mm/yyyy 23:59:59~~


