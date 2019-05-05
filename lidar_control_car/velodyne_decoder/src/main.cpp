#include <ros/ros.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_types.h>
#include <pcl/point_cloud.h>

sensor_msgs::PointCloud2 scan;
ros::Publisher *lidar_pub;

void LidarCallBack(const sensor_msgs::PointCloud2 &msg)
{
    int num = 0;
    double x = 0;
    double y = 0;
    double z = 0;

    pcl::PointCloud<pcl::PointXYZI> cloud;
    pcl::PCLPointCloud2 pcl_pc;
    pcl_conversions::toPCL(msg, pcl_pc);
    pcl::fromPCLPointCloud2(pcl_pc, cloud);
    pcl::PointCloud<pcl::PointXYZI> temp_cloud;
    pcl::PointXYZI p;

    for(int i = 0;i < cloud.points.size();i ++)
    {
        x = cloud.points.at(i).x;
        y = cloud.points.at(i).y;
        z = cloud.points.at(i).z;

        double pitch = atan2(z,hypot(x,y))*180/3.14159;
        if(pitch < 1.0 && pitch > -1.0)
        {
            p.x = x;
            p.y = y;
            p.z = z;
            temp_cloud.points.push_back(p);
        }
    }

    sensor_msgs::PointCloud2 output;
    pcl::PCLPointCloud2 pcl_pc2;
    pcl::toPCLPointCloud2(temp_cloud,pcl_pc2);
    pcl_conversions::fromPCL(pcl_pc2, output);
    output.header.frame_id = "velodyne";
    output.header.stamp = msg.header.stamp;

    lidar_pub->publish(output);
}

int main(int argc,char *argv[])
{
    ros::init(argc,argv,"velodyne_decoder_node");
    ros::NodeHandle nh;
    ros::Rate loop_rate(10.0);
    lidar_pub = new ros::Publisher();
    *lidar_pub = nh.advertise<sensor_msgs::PointCloud2>("/velodyne_scan",10);
    ros::Subscriber points_sub = nh.subscribe("/velodyne_points",10,LidarCallBack);

    while(ros::ok())
    {
        ros::spinOnce();
        loop_rate.sleep();
    }
    return 0;
}
