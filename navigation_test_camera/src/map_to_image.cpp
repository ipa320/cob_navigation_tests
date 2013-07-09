#include "ros/ros.h"
#include "sensor_msgs/Image.h"
#include "nav_msgs/OccupancyGrid.h"


class MapToImage
{
public:
	ros::NodeHandle nh;

	ros::Publisher topicPub_image;
	ros::Subscriber topicSub_map;

	MapToImage()
	{
		topicPub_image = nh.advertise<sensor_msgs::Image>("image", 1);
		topicSub_map = nh.subscribe("map", 1, &MapToImage::mapCallback, this);
	}

	void mapCallback(const nav_msgs::OccupancyGrid::ConstPtr& msg)
	{
		sensor_msgs::Image image;

		//TODO: do some fancy opencv stuff with map to convert it into an image message
		// maybe you need map metadata for it?

		topicPub_image.publish(image);
	}
};

int main(int argc, char **argv)
{

	ros::init(argc, argv, "map_to_image");

	MapToImage mti;

	ros::spin();

	return 0;
}
