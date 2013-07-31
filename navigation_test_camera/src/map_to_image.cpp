#include "ros/ros.h"
#include "sensor_msgs/Image.h"
#include "nav_msgs/OccupancyGrid.h"
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>


class MapToImage
{
public:
	ros::NodeHandle nh;

	ros::Subscriber topicSub_map_;
	image_transport::Publisher img2D_pub_;
	boost::shared_ptr<image_transport::ImageTransport> image_transport_1_;

	MapToImage(ros::NodeHandle& nh)
	{
		image_transport_1_ = boost::shared_ptr<image_transport::ImageTransport>(new image_transport::ImageTransport(nh));
		img2D_pub_= image_transport_1_->advertise("image", 1);
		topicSub_map_ = nh.subscribe("map", 1, &MapToImage::mapCallback, this);
	}

	void mapCallback(const nav_msgs::OccupancyGrid::ConstPtr& msg)
	{
		int width = msg->info.width;
		int height = msg->info.height;
		
		cv::Mat cv_image(width, height, CV_8UC3);
		std::string color_image_encoding_ = "bgr8";
		int nChannels = cv_image.channels();

		//TODO: do some fancy opencv stuff with map to convert it into an image message
		// maybe you need map metadata for it?
		unsigned char* p_cv_image = 0;
		const int8_t* p_grid_data = &(msg->data[0]);

		for (int i=0; i<height; i++)
		{
			p_cv_image = cv_image.ptr(i);
			p_grid_data = &(msg->data[i*width]);
			for (int j=0; j<width; j++)
			{
				int color_value = (p_grid_data[j]/100)*255;
				p_cv_image[nChannels*j+0] = color_value;
				p_cv_image[nChannels*j+1] = color_value;
				p_cv_image[nChannels*j+2] = color_value;
			}
		}
		
		cv_bridge::CvImage cv_ptr;
        cv_ptr.image = cv_image;
        cv_ptr.encoding = color_image_encoding_;
        img2D_pub_.publish(cv_ptr.toImageMsg());
	}
};

int main(int argc, char **argv)
{

	ros::init(argc, argv, "map_to_image");
	ros::NodeHandle nh;

	MapToImage mti(nh);

	ros::spin();

	return 0;
}
