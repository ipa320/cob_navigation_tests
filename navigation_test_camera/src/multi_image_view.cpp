#include <ros/ros.h>
#include <cv_bridge/cv_bridge.h>
#include <boost/thread/mutex.hpp>

#include <sensor_msgs/Image.h>
#include <sensor_msgs/CameraInfo.h>

#include <image_transport/image_transport.h>
#include <image_transport/subscriber_filter.h>

#include <message_filters/subscriber.h>
#include <message_filters/sync_policies/approximate_time.h>
#include <message_filters/synchronizer.h>
#include <message_filters/time_synchronizer.h>

using namespace message_filters;
using namespace sensor_msgs;
typedef sync_policies::ApproximateTime<sensor_msgs::Image, sensor_msgs::CameraInfo> ImageSyncPolicy;

void callback(const ImageConstPtr& image, const CameraInfoConstPtr& cam_info)
{
	return;
}

int main(int argc, char **argv)
{

	ros::init(argc, argv, "multi_image_view");
	ros::NodeHandle nh;

	
	//TODO: read parameters how many image topics we have

	
	// assuming we have a variable amount of image topics in a list, e.g. [/stereo/left/image_raw, /stereo/right/image_raw, /cam3d/rgb/image_color], we need to:
	// (i)   create a callback for each of them
	// (ii)  keep a copy of the last image from every topic
	// (iii) aggregate all images into one multi_view
	// (iv)  publish the multi_view image

	std::vector<std::string> vec_camera_info_topics;
	std::vector<std::string> vec_camera_topics;
	
	vec_camera_topics.push_back("/stereo/left/image_raw");
	vec_camera_info_topics.push_back("/stereo/left/camera_info");
	
	vec_camera_topics.push_back("/stereo/right/image_raw");
	vec_camera_info_topics.push_back("/stereo/right/camera_info");
	
	vec_camera_topics.push_back("/cam3d/rgb/image_color");
	vec_camera_info_topics.push_back("/cam3d/rgb/camera_info");

	//TODO: register a variable amount of subscribers
	std::vector<image_transport::SubscriberFilter> vec_camera_image_sub;
	std::vector<boost::shared_ptr<image_transport::ImageTransport> > vec_image_transport;
	std::vector<message_filters::Subscriber<sensor_msgs::CameraInfo> > vec_camera_info;
	std::vector<boost::shared_ptr<message_filters::Synchronizer<ImageSyncPolicy > > > vec_image_sub_sync;
	for (unsigned int i=0; i<vec_camera_topics.size(); i++)
	{
		image_transport::SubscriberFilter camera_image_sub_i;
		boost::shared_ptr<image_transport::ImageTransport> image_transport_i = 
			boost::shared_ptr<image_transport::ImageTransport>(new image_transport::ImageTransport(nh));
		message_filters::Subscriber<sensor_msgs::CameraInfo> camera_info_sub_i;
		boost::shared_ptr<message_filters::Synchronizer<ImageSyncPolicy > > image_sub_sync_i;
		
		camera_image_sub_i.subscribe(*image_transport_i, vec_camera_topics[i], 1);
        camera_info_sub_i.subscribe(nh, vec_camera_info_topics[i], 1);
		
		image_sub_sync_i = boost::shared_ptr<message_filters::Synchronizer<ImageSyncPolicy> >(new message_filters::Synchronizer<ImageSyncPolicy>(ImageSyncPolicy(3)));
        image_sub_sync_i->connectInput(camera_image_sub_i, camera_info_sub_i);
        image_sub_sync_i->registerCallback(boost::bind(&callback, _1, _2));
		
		vec_camera_image_sub.push_back(camera_image_sub_i);
		vec_image_transport.push_back(image_transport_i);
		vec_camera_info.push_back(camera_info_sub_i);
		vec_image_sub_sync.push_back(image_sub_sync_i);
	}

	// publish multi_view images
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
