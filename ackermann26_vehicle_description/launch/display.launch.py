from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
#from launch.actions import DeclareLaunchArgument
import os
from ament_index_python.packages import get_package_share_path

def generate_launch_description():  #estandar para la comunidad de ros

    robot_description_pkg = get_package_share_path("ackermann26_vehicle_description")

    urdf_path = os.path.join(robot_description_pkg,
                             'urdf', 'mobile_robot_base.urdf.xacro')

    rviz_config_path = os.path.join(robot_description_pkg,
                                'rviz', 'config.rviz')
    
    robot_description = ParameterValue(  #convierte todo en un parametro para un nodo de ros
        Command(
            [
             'xacro ', 
             urdf_path,
            ]), value_type= str)

    robot_state_publisher = Node(   #crea el topic
        name='my_robot_state_publisher',
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    joint_state_publisher_gui = Node(
        name='another_joint_state_publisher_gui',
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
    )

    rviz_node = Node(
        name='rviz2',
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_path]
    )

    return LaunchDescription([  #esto tambien es oarte de la base haciendo código para la comunidad de ros, siempre regresar una lista de los nodos que queremos ejecutar

        robot_state_publisher,
        joint_state_publisher_gui,
        rviz_node
    ])