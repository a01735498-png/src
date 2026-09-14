from launch import LaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource 
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch_ros.descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
#from launch.actions import DeclareLaunchArgument
import os
from ament_index_python.packages import get_package_share_path

def generate_launch_description():  #estandar para la comunidad de ros

    robot_description_pkg = get_package_share_path("ackermann26_vehicle_description")

    gz_launch_path = os.path.join(get_package_share_path('ros_gz_sim'), 'launch')

    urdf_path = os.path.join(robot_description_pkg,
                             'urdf', 'mobile_robot_base.urdf.xacro')

    rviz_config_path = os.path.join(robot_description_pkg,
                                'rviz', 'config.rviz')

    gz_bridge_config_path = os.path.join(get_package_share_path('ackermann26_vehicle_gazebo'),
                                        'config', 'ros_bridge.yaml')
    
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

    gz_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            gz_launch_path,
            "/gz_sim.launch.py"
        ]), launch_arguments={'gz_args': 'empty.sdf -r -v 4'}.items()
    )

    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_path]
    ) 

    gz_create_entity_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', '/robot_description']
    )

 
    gz_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': gz_bridge_config_path}]
    )
 

    return LaunchDescription([  #esto tambien es oarte de la base haciendo código para la comunidad de ros, siempre regresar una lista de los nodos que queremos ejecutar

        robot_state_publisher,
        rviz2_node,
        gz_sim_launch,
        gz_create_entity_node,
        gz_bridge_node
    ])