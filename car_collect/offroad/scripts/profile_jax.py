# used for code profiling 
# evaluate computation time of MPPI
# import rospy
import socket
# from sensor_msgs.msg import NavSatFix, Joy
# from sensor_msgs.msg import Image, PointCloud2, Imu
# from nav_msgs.msg import Odometry
# from scipy.optimize import minimize

import threading
import time
import json
import os
import struct
from datetime import datetime
import numpy as np
# import ros_numpy
from copy import deepcopy
import pickle
import math
from termcolor import colored

# from fusion_engine_client.parsers import FusionEngineDecoder
# from fusion_engine_client.messages import PoseMessage
from offroad import OFFROAD_DATA_DIR
# from car_dynamics.analysis import rotate_point
# from car_dynamics.models_torch import MLP
# from car_dynamics.controllers_torch import PIDController
# from ..utils import keyboard_server

import warnings
width = 336
height = 188
SAVE_FREQ = 10
BUFFER_SIZE = 8
num_log = 0
DT = 0.05
# DT = 0.05
N_ROLLOUTS = 10000
H = 40
SIGMA = 1.0
VEL_ALPHA = 0.8
velocity = 0.0
prev_x = 0.0
prev_y = 0.0
prev_psi = 0.0
controller_type = 'mppi-dbm' # mppi-nn, mppi-kbm, pid, debug
# controller_type = 'mppi-kbm' # mppi-nn, mppi-kbm, pid, debug
# controller_type = 'pid' # mppi-nn, mppi-kbm, pid, debug
# controller_type = 'teleop' # mppi-nn, mppi-kbm, pid, debug, random_walk
# controller_type = 'mppi-nn-end2end-trunk' # mppi-nn, mppi-kbm, pid, debug, random_walk
# trajectory_type = 'circle' # (counter-)circle/oval, straight, center
trajectory_type = 'counter oval' # (counter-)circle/oval, straight, center
# trajectory_type = 'center' # (counter-)circle/oval, straight, center
K_vel = 4.
K_steer = 4.
K_w = 4.
SPEED = 2.0
time_complement = 0.0
MAX_VEL = 8.
PID_KP = 5.0
PID_KI = 0.0
PID_KD = 0.05
MPPI_STEER_PROJ = .43
# 。45 for clockwise, .48 for counter
MPPI_STEER_SHIFT = 0.17
DELAY=2
waypoint_projection_shift_time = DT * .0
len_history = 2
LF = .16
LR = .15
L = LF+LR
RECOVOER_TIME = 2
RECOVER_COUNTDOWN = 2
WITHOUT_VICON = True
# For data collection

import jax
import jax.numpy as jnp
key = jax.random.PRNGKey(0)
print("DEVICE", jax.devices())

def steering_to_ros_command(command: float, calibrate=False):
    # check calibrate.ipynb
    #   , we found the maximum symmetric range to be [-0.75, 0.635]
    if calibrate:
        a = 0.7225
        b = -0.0375
        return a * command + b
    else:
        return command



    
if 'mppi' in controller_type:
    from car_dynamics.models_jax import DynamicBicycleModel, DynamicParams
    from car_dynamics.controllers_jax import MPPIParams, MPPIController, rollout_fn_select, reward_track_fn
    
   
    mppi_params = MPPIParams(
        sigma = 1.0,
        gamma_sigma=0.0,
        gamma_mean = 1.0,
        discount=1.,
        sample_sigma = 0.5,
        lam = 0.01,
        n_rollouts=N_ROLLOUTS,
        H=H,
        a_min = [-1., -1.],
        a_max = [1., 1.],
        a_mag = [0.125, 1.], # 0.1, 0.35
        a_shift = [0.325, 0.],
        delay=DELAY,
        len_history=len_history,
        debug=False,
        fix_history=False,
        num_obs=6,
        num_actions=2,
    )
    if 'dbm' in controller_type:
        model_params = DynamicParams(num_envs=N_ROLLOUTS, DT=DT,Sa=0.36, Sb=0.03, K_FFY=5, K_RFY=5, Ta=8., Tb=-1.)
        dynamics = DynamicBicycleModel(model_params,)
        rollout_fn = rollout_fn_select('dbm', dynamics, DT, L, LR)
        
    else:
        raise NotImplementedError
    
    print(rollout_fn)
        
    # sigmas = torch.tensor([SIGMA] * 2)
    # a_cov_per_step = torch.diag(sigmas**2)
    # a_cov_init = a_cov_per_step.unsqueeze(0).repeat(H, 1, 1)
    # a_cov_prev =  torch.full((H, 2, 2), 3.0**2) * torch.eye(2).unsqueeze(0).repeat(H, 1, 1)

    def fn():
        return 
    
    

    mppi = MPPIController(
        mppi_params, rollout_fn, fn, key
    )



###################### Logging dir ##################
# DATA_DIR = '/home/cmu/catkin_ws/offroad/data/dataset'
timestr = time.strftime("%Y%m%d-%H%M%S")
logdir = 'data-' + timestr
os.makedirs(os.path.join(OFFROAD_DATA_DIR, logdir),exist_ok=True )

#####################################################

car_state = dict(
                    obs=None,
                    date=None,
                    time=None, 
                 vicon_loc=None,
                #  gps_vel=None,
                 left_rgb=None,
                 right_rgb=None,
                 lidar=None,
                 imu=None,
                 zed2_odom=None,
                 vesc_odom=None,
                 throttle=0.0,
                 steering=0.0,
                 velocity = 0.0,
                 recover=False,
            )

teleop_state = dict( throttle = 0., steering = 0. )

dataset = []

print("init")
####### VICON Callback ####################
def update_vicon_placeholder():
    
    while True :
        pose_x = np.random.uniform(-1, 3) * 0.
        pose_y = np.random.uniform(-1, 3) * 0.
        pose_yaw = np.random.uniform(-np.pi, np.pi) * 0.
        car_state['vicon_loc'] = [pose_x, pose_y, pose_yaw]
        time.sleep(0.001)
        # print(colored(f"received - {car_state['vicon_loc']}", "green"))



########### Logging Fn ######################

def dumpe_file(name, data):
    def fn():
        with open(name, "wb") as f:
            # json.dump(data, f)
            pickle.dump(data, f)
        # print(f"[INFO] {data[0]['time']}, {data[0]['date']}")
    return fn

def logging():
    global dataset, num_log
    # print(len(dataset))
    if len(dataset) > SAVE_FREQ:
        # print(os.path.join(DATA_DIR, logdir, f"log{num_log}.json"))
        dataset2 = dataset[:SAVE_FREQ]
        dataset = dataset[SAVE_FREQ:]
        # print([d['time'] for d in dataset])
        assert id(dataset2) != id(dataset)
        # print(dataset)
        print("start to log")
        save_threading = threading.Thread(target=dumpe_file(os.path.join(OFFROAD_DATA_DIR, logdir, f"log{num_log}.pkl"), dataset2))
        save_threading.start()
        save_threading.join()
        # with open(os.path.join(DATA_DIR, logdir, f"log{num_log}.json"), "w") as f:
        #     json.dump({'test':dataset2}, f)
            # json.dump(dict(data=dataset[:10]), f)
        # print("after save")
        # dataset = dataset[10:]
        num_log += 1
        print("saved", num_log, "logs")

if 'teleop' in controller_type or 'random_walk' in controller_type:
    TCP_IP = "0.0.0.0"  # Replace with the IP address of your laptop
    TCP_PORT = 15214  # Replace with the desired port number
    KeyboardConnect = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    KeyboardConnect.bind((TCP_IP, TCP_PORT))
    
def keyboard_server(teleop_dict):
    BUFFER_SIZE = 8
    while True:
        data, addr = KeyboardConnect.recvfrom(BUFFER_SIZE)
        if not data:
            break
        unpacked_data = struct.unpack('ff', data)
        teleop_dict['throttle'] = unpacked_data[0]
        teleop_dict['steering'] = unpacked_data[1]
    while True:
        print("BREAK")

#############################################

    
def reference_vel(t):
    if controller_type == 'pid' and t < 0.5:
        return 0
    return SPEED

def reference_traj(t):
    if trajectory_type == 'circle':
        if controller_type == 'debug':
            if t < .4:
                t = .1
            else:
                t -= .2
        # global total_angle
        center_circle = (1., 1.2)
        circle_radius = 1.3
        angle = -np.pi/2  - circle_radius * SPEED * t
        return np.array([center_circle[0] + circle_radius * np.cos(angle),
                            center_circle[1] + circle_radius * np.sin(angle)])
        
    elif trajectory_type == 'counter circle':
        if controller_type == 'debug':
            if t < .4:
                t = .1
            else:
                t -= .2
        # global total_angle
        center_circle = (1., 1.2)
        circle_radius = 1.3
        angle = -np.pi/2  + circle_radius * SPEED * t
        return np.array([center_circle[0] + circle_radius * np.cos(angle),
                            center_circle[1] + circle_radius * np.sin(angle)])
    elif trajectory_type == 'oval':
        if controller_type == 'debug':
            if t < .4:
                t = .1
            else:
                t -= .2
        center = (0.9, 1.0)
        x_radius = 1.2
        y_radius = 1.4

        # Assuming t varies from 0 to 2π to complete one loop around the oval
        angle = -np.pi/2  - x_radius * SPEED * t

        x = center[0] + x_radius * np.cos(angle)
        y = center[1] + y_radius * np.sin(angle)

        return np.array([x, y])

    elif trajectory_type == 'counter oval':
        if controller_type == 'debug':
            if t < .4:
                t = .1
            else:
                t -= .2
        center = (0.9, 1.1)
        x_radius = 1.2
        y_radius = 1.4

        # Assuming t varies from 0 to 2π to complete one loop around the oval
        angle = -np.pi/2  + x_radius * SPEED * t

        x = center[0] + x_radius * np.cos(angle)
        y = center[1] + y_radius * np.sin(angle)

        return np.array([x, y])

    elif trajectory_type == 'straight':
        start = np.array([-0.7, -0.2])
        end = np.array([2., 3.5])
        angle_ = np.arctan2(end[1] - start[1], end[0] - start[0])
        time_length = np.linalg.norm(end-start) / SPEED
        if t < 0:
            t = 0
        if t > time_length:
            t = time_length
        x = start[0] + SPEED * t * np.cos(angle_)
        y = start[1] + SPEED * t * np.sin(angle_)
        return np.array([x, y])
    elif trajectory_type == 'center':
        return np.array([1., 1.2])
    else:
        raise NotImplementedError


def distance_to_trajectory(t, p0, trajectory_func):
    x, y = trajectory_func(t)
    return np.sqrt((x - p0[0])**2 + (y - p0[1])**2)


def get_steer_error(obs, goal):
    # psi = obs[2]
    psi = obs[4]
    psi_des = np.arctan2(goal[1] - obs[1], goal[0] - obs[0])
    err = psi_des - psi
    # err = (err + np.pi) % (2 * np.pi) - np.pi
    while err > np.pi:
        err -= 2 * np.pi
    while err < -np.pi:
        err += 2 * np.pi
    # print(psi, psi_des, err)
    return err


def joystick_controller():
    
    if 'mppi' in controller_type \
        or 'pid' in controller_type:
        waypoint_t_list = np.arange(-np.pi*3-DT, np.pi*4+DT, 0.01)
        waypoint_list = np.array([reference_traj(t) for t in waypoint_t_list])
    

        
    goal_ptr = 0
    header_info = dict(goal_list=[],controller=controller_type, trajectory=trajectory_type,
                       pid=dict(kp=PID_KP,ki=PID_KI,kd=PID_KD, max_vel=MAX_VEL),
                       mppi=dict(proj=MPPI_STEER_PROJ, shift=MPPI_STEER_SHIFT, max_vel=MAX_VEL,delay=DELAY, config=None),
                       tag='identify vicon discount error',)
    with open(os.path.join(OFFROAD_DATA_DIR, logdir, f"header.json"), "w") as f:
        json.dump(header_info, f)
        
    delta_t = DT
    t_ = 0.
    goal_list = []
    targets = []
    pid_recover = False
    vicon_recover = False
    lost_count = 0
    boundary_count = 0
    vx = 0.
    vy = 0.
    omega = 0.
 
    time_dict = dict(
        total = [],
        mppi = [],
        mppi_total = [],
        mppi_sample = [],
        mppi_rollout = [],
        mppi_reward = [],
        mppi_misc = [],
    )
    
    for idx_ in range(50):
        print(idx_)
        global pub, car_state, prev_x, prev_y, prev_psi, velocity, time_complement, RECOVOER_TIME
        # now = rospy.Time.now()
        # cmd = Joy()
        # cmd.header.stamp = now
        # cmd.buttons = [0,0,0,0,0,0,1,0,0,0,0]
        # car_state['time'] = datetime.now()
        car_state['time'] =time.time()
        car_state['date'] = datetime.now()
        
        # Calculate time difference
        
        # print(f"car state: {car_state['vicon]}")
        if car_state['vicon_loc'] is None:
            print(colored("DISCOUNNECT", "red"))
            continue
        
        # print("before", car_state['vicon_loc'])
        st_control = time.time()
        # Calculate position differences
        delta_x = car_state['vicon_loc'][0] - prev_x
        delta_y = car_state['vicon_loc'][1] - prev_y
        omega_ = car_state['vicon_loc'][2] - prev_psi
        omega_ = np.arctan2(np.sin(omega_), np.cos(omega_)) / delta_t
        # Check direction
        vec_pos = np.array([delta_x, delta_y])
        
        # v_vec = vec_pos / delta_t
        v_vec = vec_pos / delta_t
        
      
        vx_ = v_vec[0] * np.cos(car_state['vicon_loc'][2]) + v_vec[1] * np.sin(car_state['vicon_loc'][2])
        vy_ = v_vec[1] * np.cos(car_state['vicon_loc'][2]) - v_vec[0] * np.sin(car_state['vicon_loc'][2])
        
        vx += (vx_ - vx) * K_vel
        vy += (vy_ - vy) * K_vel
        omega += (omega_ - omega) * K_w
        
        vel_angle = np.arctan2(delta_y, delta_x)
        vec_car = np.array([np.cos(car_state['vicon_loc'][2]), np.sin(car_state['vicon_loc'][2])])
        idc = np.dot(vec_pos, vec_car)

        if idc >= 0:
            idc = 1.0
        else:
            idc = -1.0

        # Calculate velocity
        velocity = velocity \
            + (idc * math.sqrt(delta_x**2 + delta_y**2) / delta_t - velocity) * VEL_ALPHA
        
        prev_x = car_state['vicon_loc'][0]
        prev_y = car_state['vicon_loc'][1]
        prev_psi = car_state['vicon_loc'][2]
        
        velocity_norm = 0. if velocity < 0. else velocity
        
        
        obs = np.array([
            car_state['vicon_loc'][0],
            car_state['vicon_loc'][1],
            car_state['vicon_loc'][2],
            velocity_norm,
            vel_angle,
        ])
        
        obs_mppi = np.array([
            car_state['vicon_loc'][0],
            car_state['vicon_loc'][1],
            car_state['vicon_loc'][2],
            vx,
            vy,
            omega,
        ])
        
        start_to_control = time.time()
        target_pos = reference_traj(t_)
        
        car_state['recover'] = False
       
        if 'mppi' in controller_type:
            ## TODO: Project waypoints based on current position
            # t_closed = find_projection(obs[:2], reference_traj)[0]
            distance_list = np.linalg.norm(waypoint_list - obs[:2], axis=-1)
            # import pdb; pdb.set_trace()
            t_idx = np.argmin(distance_list)
            t_closed = waypoint_t_list[t_idx]
            target_pos_list = [reference_traj(waypoint_projection_shift_time + t_closed + i*DT*.75) for i in range(H+DELAY+1)]
            target_pos = target_pos_list[0]
            # import pdb; pdb.set_trace()
            target_pos_tensor = jnp.array(target_pos_list)
            # if 'kbm' in controller_type:
            #     dynamics_kbm.reset()
            st_mppi = time.time()
            print("MAIN START", st_mppi)
            # action, mppi_info = mppi(obs[:4], reward_track_fn(target_pos_tensor, SPEED))
            # print("OBS", obs_mppi)
            action, mppi_info = mppi(obs_mppi, target_pos_tensor)
            # print(mppi_info['t_debug']['MPPI_START'], mppi_info['t_debug']['MPPI_END'])
            
            t_mppi = time.time() - st_mppi
            print("MAIN END", time.time())
            print(colored(f"mppi time - {t_mppi}", "green"))
            # action = action
            # import pdb; pdb.set_trace()
            car_state['mppi_actions'] = None
            # print(car_state['mppi_actions'])
            car_state['targets'] = np.array(target_pos_list).tolist()
            
            time_dict['mppi'].append(t_mppi)
            # {'sample': t_sample, 'rollout': t_rollout, 'calc_reward': t_calc_reward, 'misc': t_misc}
            time_dict['mppi_sample'].append(mppi_info['t_debug']['sample'])
            time_dict['mppi_rollout'].append(mppi_info['t_debug']['rollout'])
            time_dict['mppi_reward'].append(mppi_info['t_debug']['calc_reward'])
            time_dict['mppi_misc'].append(mppi_info['t_debug']['misc'])
            time_dict['mppi_total'].append(mppi_info['t_debug']['total'])
            
            
        elif 'debug' in controller_type:
            action = np.array([.1, .0])
        

    
        print("action", action)  
        # print(colored(f"target: {target_pos}", "red"))
        print(colored(f"pos: {obs[:2]}, yaw: {obs[2]}, vel: {obs[3]}", 'blue'))
        if time.time() - start_to_control > DT:
            # action *= .0
            print("time out", "control time", time.time() - start_to_control)
        # action *= 0.
        
        if 'mppi-nn' in controller_type:
            mppi.feed_hist(obs, action)
            
        car_state['obs'] = np.concatenate([obs, target_pos])
        
      
        # action *= 0.
        car_state['throttle'] = action[0]
        car_state['steering'] = action[1]
        
        
        ################### Publish Command to ROS #############################
        ros_command_steering = steering_to_ros_command(car_state['steering'], calibrate=False)
        # ros_command_steering = car_state['steering']
        # print("ROS Command", car_state['throttle'], ros_command_steering)
        # print(car_state['throttle'],ros_command_steering)
        # cmd.axes = [0.,car_state['throttle'],ros_command_steering,0.,0.,0.]
        # # cmd.axes = [0.,forward_speed,(steering/max_steering),steering/max_steering,0.,0.]
        # # print("REAL COMMAND", cmd)
        # pub.publish(cmd)
        ########################################################################
        
        dataset.append(car_state.copy()) 
        goal_list.append(target_pos)
            
            
        # # print("pub", throttle, steering)
        # if car_state['imu'] is not None and \
        #         car_state['zed2_odom'] is not None:
        #     # print("start to collect", car_state['time'])
        #     # print(f"yaw, imu:{quaternion_to_euler(car_state['imu']['orientation'])[2]}, zed:{quaternion_to_euler(car_state['zed2_odom']['orientation'])[2]}, vesc:{quaternion_to_euler(car_state['vesc_odom']['orientation'])[2]}")
        #     # print("after", car_state['vicon_loc'])
        #     dataset.append(car_state.copy()) 
        #     goal_list.append(target_pos)
            
        #     # if len(dataset) > 1:
        #         # print(dataset[-2]['time'], dataset[-1]['time'])
        # # print("before logging!")
        logging()
        time_complement = time.time() - st_control
        # print(time_complement)
        if DT > time_complement:
            time.sleep(DT - time_complement)
        else:
            ...
        # print("time complement", time_complement)
        # assert DT > time_complement
        # time.sleep(DT)
        
        t_ += time.time() - st_control
        
        if trajectory_type == 'straight' and t_ > 24:
            break
        if t_ > 1000:
            break
            
        delta_t = time.time() - st_control
        time_dict['total'].append(delta_t)
        # print(colored(f"[INFO] delta time: {delta_t}", "red"))
    
    # with open(os.path.join(OFFROAD_DATA_DIR, logdir, f"time.json"), "w") as f:
    #     json.dump(time_dict, f)  
        
    print("MEAN MPPI TIME", np.mean(time_dict['mppi_total'][5:]))
    print("MEAN MPPI TIME", np.mean(time_dict['mppi'][5:]))
    # print(time_dict['mppi_total'])
    print("MEAN ROLLOUT TIME", np.mean(time_dict['mppi_rollout'][5:]))
    print("MEAN sample TIME", np.mean(time_dict['mppi_sample'][5:]))
    print("MEAN reward TIME", np.mean(time_dict['mppi_reward'][5:]))
    print("MEAN misc TIME", np.mean(time_dict['mppi_misc'][5:]))
        
    print("done")
    return

###############################################


################################################
        
if __name__ == '__main__':
    print("start")
    # rospy.init_node('controller', anonymous=True, disable_signals=True)
    # global pub
    # pub = rospy.Publisher('/vesc/joy',Joy)
    
    if 'teleop' in controller_type or 'random_walk' in controller_type:
        keyboard_thread = threading.Thread(target=keyboard_server, args=(teleop_state, ))
        keyboard_thread.start()
    
    if WITHOUT_VICON:
        vicon_fn = update_vicon_placeholder
    else:
        vicon_fn = update_vicon
    vicon_thread = threading.Thread(target=vicon_fn)
    vicon_thread.start()

    joystick_thread = threading.Thread(target=joystick_controller)
    joystick_thread.start()


    ## Camera node
    # rospy.Subscriber('/front_camera/zed2/zed_node/left/image_rect_color', Image, left_rgb_callback, queue_size = 1)
    # rospy.Subscriber('/front_camera/zed2/zed_node/right/image_rect_color', Image, right_rgb_callback, queue_size = 1)
    # rospy.Subscriber('/velodyne_points', PointCloud2, lidar_callback, queue_size = 1)
    # rospy.Subscriber('/front_camera/zed2/zed_node/imu/data', Imu, imu_callback, queue_size = 1)
    # rospy.Subscriber('/vesc/odom', Odometry, vesc_odom_callback, queue_size = 1)
    # rospy.Subscriber('/front_camera/zed2/zed_node/odom', Odometry, zed2_odom_callback, queue_size = 1)

    # rospy.spin()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        vicon_thread.join()
        if 'teleop' in controller_type or 'random_walk' in controller_type:
            keyboard_thread.join()
        joystick_thread.join()
        vicon_thread.join()