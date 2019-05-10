# three_omni
try to control A three_omni_robot
<br/>
作为三轮全向轮工程文件
<br/>
## 车体介绍
由三轮全向轮作为移动结构
使用TCP通信控制<br/>上位机和小车之间严格按照[通信协议](https://github.com/marktlen/three_omni/blob/master/%E4%B8%89%E8%BD%AE%E5%85%A8%E5%90%91%E5%BA%95%E7%9B%98%E5%8D%8F%E8%AE%AEv0.2.pdf)进行控制<br/>
小车通过路由器接收数据报，将数据报给解析器，让解析器控制3个电机的运动
<br/>
里程计通过路由器发送数据报，给上位机3个轮子的里程数据
<br/>
## 通信注意事项
遥控器和TCP通信不能同时进行，同时控制时会优先服从TCP通信控制
<br/>
里程计只会在每条动作执行完成后反馈一次
<br/>
里程计初始值是随机数需要过滤掉以免影响以后计算
<br/>
注意tcp通信的频率，如果通信过快底盘会处理不过来
<br/>
## 运行环境说明
需要安装ROS和常用的ROS的依赖
<br/>
## 文件作用说明
ROS three_omni是录制的调试产生的参数
<br/>
里面包含一个键盘控制的python文件
<br/>
和一个用于硬件测试的python文件
<br/>
### src下包含两个包
* controlcar文件夹是最新的底盘控制文件
* omni_gazebo是车体的底盘仿真模型文件
## 快速进行车辆控制
<br/>

    $cd 工作路径下
    $source devel/setup.bash

<br/>  
新建终端，启动底盘的tcp通信控制和里程计反馈的topic发布端<br/>

    $python /src/omni_gazebo/src1.13version.py
   
<br/>
再新建一个，启动简单的键盘控制程序，测试是否成功与底盘通信<br/>

    $python /src/omni_gazebo/src/robot_keyboard_teleop.py
    
## 进行简单的slam_gmapping建图定位
<br/>
请在工作空间下安装[rplidar_ros](https://github.com/robopeak/rplidar_ros)包
<br/>

    $git clone https://github.com/robopeak/rplidar_ros.git

<br/>
安装完成后，将包里面的src/node.cpp中的修改为车体半径(0.59)
<br/>

    78 scan_msg.range_min = 0.59;

<br/>
完成后请重新编译工作空间,现在可以启动slam_gmapping了
<br/>

    $roslaunch omni_gazebo robot_slam_gmapping.launch

<br/>
启动底盘驱动
<br/>

    $python /src/omni_gazebo/src1.13version.py

<br/>
建议使用新的键盘控制文件,保证建图效果,注意：点击键盘后小车会一直执行这个命令，一定要用"k"键停止!!
<br/>

    $python /src/omni_gazebo/src/keyboard_teleop_onestep.py

<br/>
