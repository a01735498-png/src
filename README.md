# Ackermann26 Vehicle

ROS 2 model and Gazebo simulation of a small Ackermann-steered ground vehicle
(QCar-style platform): 4-wheel chassis with front-wheel Ackermann steering,
CSI cameras, IMU, RealSense RGB-D camera, and a 360° LiDAR.

This repository is meant to be cloned directly as the `src/` folder of a
colcon workspace (it is not nested inside its own `src/` subfolder).

## Packages

| Package | Purpose |
|---|---|
| [`ackermann26_vehicle_description`](ackermann26_vehicle_description) | Xacro/URDF model of the vehicle (chassis, wheels, steering, sensor links) and an RViz-only launch file to visualize it (no physics). |
| [`ackermann26_vehicle_gazebo`](ackermann26_vehicle_gazebo) | Spawns the vehicle in Gazebo (`gz sim`) and bridges topics (`cmd_vel`, odometry, joint states, IMU, cameras, LiDAR) between Gazebo and ROS 2. |

## Prerequisites

- **ROS 2** (Jazzy or newer recommended) sourced in your shell.
- **Gazebo (`gz sim`, Harmonic or compatible)** with the `ros_gz` bridge
  packages installed: `ros_gz_sim`, `ros_gz_bridge`.
- `xacro`, `robot_state_publisher`, `joint_state_publisher_gui`, `rviz2`.

On Debian/Ubuntu with ROS 2 already installed, the runtime dependencies can
usually be pulled in with:

```bash
sudo apt install ros-$ROS_DISTRO-xacro ros-$ROS_DISTRO-robot-state-publisher \
                  ros-$ROS_DISTRO-joint-state-publisher-gui ros-$ROS_DISTRO-rviz2 \
                  ros-$ROS_DISTRO-ros-gz-sim ros-$ROS_DISTRO-ros-gz-bridge
```

## Build

```bash
# Create a colcon workspace and clone this repo AS its src/ folder
mkdir -p ~/sm26_ws
cd ~/sm26_ws
git clone https://github.com/a01735498-png/src.git src

# Resolve any missing dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build
colcon build

# Source the workspace
source install/setup.bash
```

## Launch

**Visualize the model in RViz only (no physics)** — use this to check that
the model, colors, and joint limits look right:

```bash
ros2 launch ackermann26_vehicle_description display.launch.py
```

A window with sliders for each wheel/steering joint (`joint_state_publisher_gui`)
opens alongside RViz so you can move the joints by hand.

**Run the full physics simulation in Gazebo, bridged to ROS 2:**

```bash
ros2 launch ackermann26_vehicle_gazebo gz_sim.launch.py
```

This opens Gazebo with the vehicle spawned in an empty world, plus RViz.
Drive it by publishing to `/cmd_vel`, e.g.:

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.3}, angular: {z: 0.2}}"
```

Sensor data is available on the standard ROS 2 topics once bridged, e.g.
`/scan` (LiDAR), `/imu`, `/front_camera/image_raw`, `/realsense/depth/image_raw`,
and `/odometry`. See
[`config/ros_bridge.yaml`](ackermann26_vehicle_gazebo/config/ros_bridge.yaml)
for the full topic list.

## Repository layout

```
src/                                        (this repository)
├── ackermann26_vehicle_description/
│   ├── urdf/        # Xacro model: common_properties, base model, Gazebo plugins/sensors
│   ├── launch/       # display.launch.py (RViz only)
│   └── rviz/         # Saved RViz view configuration
├── ackermann26_vehicle_gazebo/
│   ├── config/       # ros_bridge.yaml (Gazebo <-> ROS 2 topic bridge)
│   └── launch/       # gz_sim.launch.py (spawn + bridge + RViz)
├── .gitignore
└── README.md
```

## License

Apache-2.0 — see [`ackermann26_vehicle_description/LICENSE`](ackermann26_vehicle_description/LICENSE)
and [`ackermann26_vehicle_gazebo/LICENSE`](ackermann26_vehicle_gazebo/LICENSE).
