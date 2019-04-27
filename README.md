# three_omni
try to control A three_omni_robot
<br/>
作为三轮全向轮工程文件
<br/>
## 车体介绍
由三轮全向轮作为移动结构
使用TCP通信控制，<a href = “three_omni/三轮全向底盘协议v0.2.pdf”>通信协议</a>
通过路由器发送数据报，将数据报给解析器，让解析器控制3个电机的运动
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
<br/>
## 快速进行车辆控制
<br/>
'$cd 工作路径下'
<br/>
'$source 不要忘了source一下'
<br/>
启动ros主节点
<br/>
'$roscore'<br/>
新建终端，启动底盘的tcp通信控制和里程计反馈的topic发布端<br/>
'$python /ROS three_omni/1.13version.py'<br/>
再新建一个，启动简单的键盘控制程序，测试是否成功与底盘通信<br/>
'$python /ROS three_omni/robot_keyboard_teleop.py'<br/>
