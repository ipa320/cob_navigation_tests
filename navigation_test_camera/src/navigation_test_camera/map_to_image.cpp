#include "ros/ros.h"
#include "sensor_msgs/Image.h"
#include "nav_msgs/OccupancyGrid.h"
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <boost/thread/mutex.hpp>

class MapToImage
{
public:
	ros::NodeHandle nh;

	ros::Subscriber topicSub_map_;
	image_transport::Publisher img2D_pub_;
	cv::Mat cv_image_;
	boost::shared_ptr<image_transport::ImageTransport> image_transport_1_;
	boost::mutex mutexQ_;
	std::string color_image_encoding_;
	bool first_run_;
	
	MapToImage(ros::NodeHandle& nh)
	{
		image_transport_1_ = boost::shared_ptr<image_transport::ImageTransport>(new image_transport::ImageTransport(nh));
		img2D_pub_= image_transport_1_->advertise("image", 1);
		topicSub_map_ = nh.subscribe("map", 1, &MapToImage::mapCallback, this);
		
		color_image_encoding_ = "bgr8";
	}

	void mapCallback(const nav_msgs::OccupancyGrid::ConstPtr& msg)
	{
		ROS_INFO("Received map");
		{
			ROS_INFO("Setting image");
			boost::mutex::scoped_lock lock( mutexQ_);
		
			int width = msg->info.width;
			int height = msg->info.height;
			
			ROS_INFO("Width %d", width);
			ROS_INFO("Height %d", height);
			
			cv_image_.create(width, height, CV_8UC3);
			int nChannels = cv_image_.channels();

			unsigned char* p_cv_image = 0;
			//const int8_t* p_grid_data = &(msg->data[0]);
			double grid_map_max_val = 100.0;

			std::vector<int> color_values(255, 0);

			for (int i=0; i<height; i++)
			{
				p_cv_image = cv_image_.ptr(i);
				//p_grid_data = &(msg->data[i*width]);
				for (int j=0; j<width; j++)
				{
					if (int(msg->data[i*width+j]) < 0)
					{
						p_cv_image[nChannels*j+0] = 0;
						p_cv_image[nChannels*j+1] = 0;
						p_cv_image[nChannels*j+2] = 255;
					}
					else
					{
						unsigned char color_value = (1.0 - (1.0/grid_map_max_val)*double(msg->data[i*width+j]))*255.0;
						color_values[int(color_value)]++;
						
						p_cv_image[nChannels*j+0] = color_value;
						p_cv_image[nChannels*j+1] = color_value;
						p_cv_image[nChannels*j+2] = color_value;
					}
				}
			}
			
			for (int i=0; i<color_values.size(); i+=3)
			{
					std::cout << i << ": " <<  color_values[i] << "           ";
					std::cout << i+1 << ": " <<  color_values[i+1] << "           ";
					std::cout << i+2 << ": " <<  color_values[i+2] << std::endl;
			}
			
			ROS_INFO("Setting image [Done]");
		}
		publish_image();
	}
	
	void publish_image()
	{
		boost::mutex::scoped_lock lock( mutexQ_);
		cv_bridge::CvImage cv_ptr;
		if (!cv_image_.empty())
		{
			ROS_INFO("Publishing image");
			cv_ptr.image = cv_image_;
			cv_ptr.encoding = color_image_encoding_;
			img2D_pub_.publish(cv_ptr.toImageMsg());
		}
	}
};

int main(int argc, char **argv)
{

	ros::init(argc, argv, "map_to_image");
	ros::NodeHandle nh;

	MapToImage mti(nh);
	
	ros::Rate r(10); // 10 hz
	while (ros::ok())
	{
	  mti.publish_image();
	  ros::spinOnce();
	  r.sleep();
	}

	return 0;
}
