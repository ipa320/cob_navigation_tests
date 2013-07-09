#include "ros/ros.h"
#include "sensor_msgs/Image.h"


int main(int argc, char **argv)
{

	ros::init(argc, argv, "multi_image_view");
	ros::NodeHandle n;

	
	//TODO: read parameters how many image topics we have

	
	// assuming we have a variable amount of image topics in a list, e.g. [/stereo/left/image_raw, /stereo/right/image_raw, /cam3d/rgb/image_color], we need to:
	// (i)   create a callback for each of them
	// (ii)  keep a copy of the last image from every topic
	// (iii) aggregate all images into one multi_view
	// (iv)  publish the multi_view image


	//TODO: register a variable amount of subscribers


	// publish cylcically current multi_view image
	ros::Rate loop_rate(10);
	while (ros::ok())
	{
		// TODO do the aggregation from all current images into one multi_view image

		// publish multi_view image
		//multi_image_pub.publish(multi_view);

		ros::spinOnce();

		loop_rate.sleep();
	}

	return 0;
}
