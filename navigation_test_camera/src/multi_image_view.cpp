#include "ros/ros.h"
#include "sensor_msgs/Image.h"


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

	std::vector<std::string> vec_cameras;
	std::vector<std::string> vec_camera_infos;
	topics.push_back("/stereo/left/image_raw");
	vec_camera_infos.push_back("/stereo/left/camera_info");
	
	topics.push_back("/stereo/right/image_raw");
	vec_camera_infos.push_back("/stereo/right/camera_info");
	
	topics.push_back("/cam3d/rgb/image_color");
	vec_camera_infos.push_back("/cam3d/rgb/camera_info");

	typedef sync_policies::ApproximateTime<sensor_msgs::Image, sensor_msgs::CameraInfo> ImageSyncPolicy;

	//TODO: register a variable amount of subscribers
	std::vector<image_transport::SubscriberFilter> vec_camera_image_sub;
	for (int i=0; i<topics.size(); i++)
	{
		image_transport::SubscriberFilter camera_image_sub_i;
		boost::shared_ptr<image_transport::ImageTransport> image_transport_i = 
			boost::shared_ptr<image_transport::ImageTransport>(new image_transport::ImageTransport(nh));
		message_filters::Subscriber<sensor_msgs::CameraInfo> camera_info_sub_i;
		boost::shared_ptr<message_filters::Synchronizer<ImageSyncPolicy > > image_sub_sync_i;
		
		camera_image_sub_i.subscribe(*image_transport_i, topics[i], 1);
        camera_info_sub_i.subscribe(node_handle_, "camera_info", 1);
		
		image_sub_sync_i = boost::shared_ptr<message_filters::Synchronizer<ImageSyncPolicy> >(new message_filters::Synchronizer<ImageSyncPolicy>(ImageSyncPolicy(3)));
        image_sub_sync_i->connectInput(camera_image_sub_i, camera_info_sub_i);
        image_sub_sync_i->registerCallback(boost::bind(&???????????????, this, _1, _2));
		
		vec_camera_image_sub_.push_back(camera_image_sub);
	}

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
