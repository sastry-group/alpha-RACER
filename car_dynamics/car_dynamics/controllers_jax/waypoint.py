import jax
import jax.numpy as jnp
import numpy as np
import pandas as pd
import yaml
import time 


def counter_circle(theta):
    center = (0., 0.)
    radius = 4.5
    return jnp.array([center[0] + radius * jnp.cos(theta),
                      center[1] + radius * jnp.sin(theta)])
    
def counter_oval(theta):
    center = (0., 0.)
    x_radius = 1.2
    y_radius = 1.4

    x = center[0] + x_radius * jnp.cos(theta)
    y = center[1] + y_radius * jnp.sin(theta)

    return jnp.array([x, y])

def get_curvature(x1, y1, x2, y2, x3, y3):
    a = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    b = np.sqrt((x3-x2)**2 + (y3-y2)**2)
    c = np.sqrt((x3-x1)**2 + (y3-y1)**2)
    s = (a+b+c)/2
    prod = (x2-x1)*(y3-y2) - (x3-x2)*(y2-y1)
    return 4*np.sqrt(s*(s-a)*(s-b)*(s-c))/(a*b*c)*np.sign(prod)

def custom_fn(theta, traj):
    while theta >= traj[-1, 0]:
        theta -= traj[-1, 0]
    i = np.sum(traj[:,0]<theta) - 1
    ratio = (theta - traj[i, 0]) / (traj[i + 1, 0] - traj[i, 0])
    x, y = traj[i, 1] + ratio * (traj[i + 1, 1] - traj[i, 1]), traj[i, 2] + ratio * (traj[i + 1, 2] - traj[i, 2])
    v = traj[i, 3] + ratio * (traj[i + 1, 3] - traj[i, 3])
    N = len(traj)
    theta = jnp.arctan2(traj[(i + 1)%N, 1] - traj[i, 1], traj[(i + 1)%N, 2] - traj[i, 2])
    curv = get_curvature(traj[i, 1], traj[i, 2], traj[(i + 1)%N, 1], traj[(i + 1)%N, 2], traj[(i + 2)%N, 1], traj[(i + 2)%N, 2])
    return jnp.array([x, y]), v, {'curv': curv}
    

def counter_square(theta):
    theta = jnp.arctan2(jnp.sin(theta), jnp.cos(theta))
    ## Generate a square
    center = (1., 2.0)
    x_radius = 4.
    y_radius = 4.
    r = jnp.sqrt(x_radius**2 + y_radius**2)
    
    if -np.pi/4 <= theta <= jnp.pi/4:
        x = center[0] + x_radius
        y = center[1] + r * jnp.sin(theta)
    elif -jnp.pi/4*3 <= theta <= -jnp.pi/4:
        x = center[0] + r * jnp.cos(theta)
        y = center[1] - y_radius
    elif -jnp.pi <= theta <= -jnp.pi/4*3 or jnp.pi/4*3 <= theta <= jnp.pi:
        x = center[0] - x_radius
        y = center[1] + r * jnp.sin(theta)
    else:
        x = center[0] + r * jnp.cos(theta)
        y = center[1] + y_radius

    return jnp.array([x, y])
    
class WaypointGenerator:
    
    def line_point_distance(self, px, py, x1, y1, x2, y2):
        """
        This function calculates the distance between a point and a line segment, also determining side.

        Args:
            px: x coordinate of the point.
            py: y coordinate of the point.
            x1: x coordinate of the first point on the line segment.
            y1: y coordinate of the first point on the line segment.
            x2: x coordinate of the second point on the line segment.
            y2: y coordinate of the second point on the line segment.

        Returns:
            A tuple containing the distance and a value indicating side (positive for left, negative for right).
        """

        # Calculate the vector along the line segment
        dx = x2 - x1
        dy = y2 - y1

        # Calculate the vector from the point to the first point on the line segment
        t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)

        return t

    def calc_shifted_traj(self, traj, shift_dist) :
        # This function calculates the shifted trajectory given the original trajectory and the shift distance.
        traj_ = np.copy(traj)
        traj_[:-1] = traj[1:]
        traj_[-1] = traj[0]
        _traj = np.copy(traj)
        _traj[1:] = traj[:-1]
        _traj[0] = traj[-1]
        yaws = np.arctan2(traj_[:,1] - _traj[:,1], traj_[:,0] - _traj[:,0])
        traj_new = np.copy(traj)
        traj_new[:,0] = traj[:,0] + shift_dist * np.cos(yaws + np.pi/2)
        traj_new[:,1] = traj[:,1] + shift_dist * np.sin(yaws + np.pi/2)
        return traj_new
    
    
    
    def __init__(self, waypoint_type: str, dt: float, H: int, speed: float):
        self.waypoint_type = waypoint_type
        
        if waypoint_type == 'counter circle':
            self.fn = counter_circle
        elif waypoint_type == 'counter oval':
            self.fn = counter_oval
        elif waypoint_type == 'counter square':
            self.fn = counter_square
        elif waypoint_type.endswith('.yaml'):
            yaml_content = yaml.load(open(waypoint_type, 'r'), Loader=yaml.FullLoader)
            centerline_file = yaml_content['track_info']['centerline_file'][:-4]
            ox = yaml_content['track_info']['ox']
            oy = yaml_content['track_info']['oy']
            self.fn = custom_fn
            df = pd.read_csv('../../ref_trajs/' + centerline_file + '_with_speeds.csv')
            df_raceline = pd.read_csv('../../ref_trajs/' + centerline_file + '_raceline_with_speeds.csv')
            self.raceline = np.array(df_raceline.iloc[:,:4]) + np.array([0, ox, oy, 0])
            self.raceline_dev = 2*np.array(df_raceline.iloc[:,4])
            # print(self.path)
            self.raceline = self.raceline[:,1:]
            self.raceline[:,:2] *= float(yaml_content['track_info']['scale'])
            # Check if waypoint_type has a substring 'num' in it to determine
            if waypoint_type.find('num') != -1:
                self.path = np.array(df.iloc[:-1,:])*yaml_content['track_info']['scale'] + np.array([0, ox, oy, 0])
            else :
                self.path = np.array(df.iloc[:,:]) + np.array([0, ox, oy, 0])
            self.path[:,-1] = speed
            self.waypoint_type = 'custom'
            self.scale = 6.5*(float(yaml_content['vehicle_params']['Lf']) + float(yaml_content['vehicle_params']['Lr']))
            # print("hahahaha: ", yaml_content['track_info']['track_width']/2.)
            self.left_boundary = self.calc_shifted_traj(self.path[:,1:], yaml_content['track_info']['track_width']/2.+0.15)
            self.right_boundary = self.calc_shifted_traj(self.path[:,1:], -yaml_content['track_info']['track_width']/2.-0.2)
        else :
            self.fn = custom_fn
            self.scale = 1.
            df = pd.read_csv('../../../lecar-car/ref_trajs/' + self.waypoint_type + '_with_speeds.csv')
            # df = pd.read_csv('../../../lecar-car/ref_trajs/' + self.waypoint_type + '_with_speeds.csv')
            print(df)
            print(np.array(df.iloc[:,:]).shape)
            self.path = np.array(df.iloc[:,[6,1,0,4]])
            self.path[:,1] -= 2.2
            self.path[:,2] -= 0.5
            self.path[:,1] *= 0.7
            self.path[:,2] *= 0.7
            self.path[:,0] *= 0.7
            self.waypoint_type = 'custom'
        # else:
        #     raise ValueError(f"Unknown waypoint_type: {waypoint_type}")
        self.dt = dt 
        self.H = H
        self.speed = speed
        if self.waypoint_type == 'custom':
            self.waypoint_t_list = jnp.arange(0, self.path[-1,0], 0.1*self.scale)
            self.waypoint_list = jnp.array([self.fn(t,self.path)[0] for t in self.waypoint_t_list])
        else :
            self.waypoint_t_list = jnp.arange(0, jnp.pi*2+dt, dt / speed)
            self.waypoint_list = jnp.array([self.fn(t) for t in self.waypoint_t_list])
        self.waypoint_list_np = np.array(self.waypoint_list)
        self.last_i = -1
        
    # def calc_lat_error(self, pos, t_closed):
    
    def generate(self, obs: jnp.ndarray, dt=-1, mu_factor=1.,body_speed=1.) -> jnp.ndarray:
        if dt < 0.:
            dt = self.dt
        # print(len(self.waypoint_list))
        pos2d = obs[:2]
        psi = obs[2]
        vel2d = obs[3:5]
        ts = time.time()
        if self.waypoint_type != 'custom':
            distance_list = jnp.linalg.norm(self.waypoint_list - pos2d, axis=-1)
            t_idx = jnp.argmin(distance_list)
            t_closed = self.waypoint_t_list[t_idx]
            target_pos_list = []
            
            magic_factor = 1./1.2
            for i in range(self.H+1):
                t = t_closed + i * dt * self.speed * magic_factor
                t_1 = t + dt * self.speed * magic_factor
                pos = self.fn(t)
                pos_next = self.fn(t_1)
                vel = (pos_next - pos) / dt
                speed_ref = jnp.clip(jnp.linalg.norm(vel), .5, 100.)
                # print(speed_ref)
                psi = jnp.arctan2(pos_next[1] - pos[1], pos_next[0] - pos[0])
                target_pos_list.append(jnp.array([pos[0], pos[1], psi, speed_ref]))
            return jnp.array(target_pos_list), None
        else :
            if self.last_i == -1:
                # print("WTF!!!!!!", pos2d, self.waypoint_list)
                distance_list = jnp.linalg.norm(self.waypoint_list - pos2d, axis=-1)
                t_idx = jnp.argmin(distance_list)
                self.last_i = t_idx
            else :
                if self.last_i + 20 < len(self.waypoint_list):
                    distance_list = jnp.linalg.norm(self.waypoint_list[self.last_i:(self.last_i+20)] - pos2d, axis=-1)
                    t_idx = jnp.argmin(distance_list) + self.last_i          
                else :
                    distance_list = jnp.linalg.norm(self.waypoint_list[self.last_i:] - pos2d, axis=-1)
                    t_idx1 = jnp.argmin(distance_list) + self.last_i
                    distance_list2 = jnp.linalg.norm(self.waypoint_list[:20] - pos2d, axis=-1)
                    t_idx2 = jnp.argmin(distance_list2)
                    d1 = distance_list[t_idx1]
                    d2 = distance_list2[t_idx2]
                    if d1 < d2:
                        t_idx = t_idx1
                    else :
                        t_idx = t_idx2 
                self.last_i = t_idx
            # print("init time: ", ts-time.time())
            t_closed = self.waypoint_t_list[t_idx]
            
            d1 = np.sqrt((self.waypoint_list[t_idx-1,0]-self.waypoint_list[t_idx,0])**2 \
                + (self.waypoint_list[t_idx-1,1]-self.waypoint_list[t_idx,1])**2)
            if d1 > 0. : 
                t1 = self.line_point_distance(pos2d[0], pos2d[1], self.waypoint_list[t_idx-1,0], self.waypoint_list[t_idx-1,1], self.waypoint_list[t_idx,0], self.waypoint_list[t_idx,1])
                side = jnp.sign((self.waypoint_list[t_idx,0]-self.waypoint_list[t_idx-1,0])*(pos2d[1]-self.waypoint_list[t_idx-1,1]) - (self.waypoint_list[t_idx,1]-self.waypoint_list[t_idx-1,1])*(pos2d[0]-self.waypoint_list[t_idx-1,0]))
                pt = self.waypoint_list[t_idx-1] + t1 * (self.waypoint_list[t_idx] - self.waypoint_list[t_idx-1])
                dist1 = np.sqrt((pos2d[0]-pt[0])**2 + (pos2d[1]-pt[1])**2) * side
                d1 *= min(1.,max(0.,t1)) - 1.
            N = len(self.waypoint_list)
            d2 = np.sqrt((self.waypoint_list[t_idx,0]-self.waypoint_list[(t_idx+1)%N,0])**2 \
                + (self.waypoint_list[t_idx,1]-self.waypoint_list[(t_idx+1)%N,1])**2)
            if d2 > 0. :
                t2 = self.line_point_distance(pos2d[0], pos2d[1], self.waypoint_list[t_idx,0], self.waypoint_list[t_idx,1], self.waypoint_list[(t_idx+1)%N,0], self.waypoint_list[(t_idx+1)%N,1])
                side = jnp.sign((self.waypoint_list[(t_idx+1)%N,0]-self.waypoint_list[t_idx,0])*(pos2d[1]-self.waypoint_list[t_idx,1]) - (self.waypoint_list[(t_idx+1)%N,1]-self.waypoint_list[t_idx,1])*(pos2d[0]-self.waypoint_list[t_idx,0]))
                pt = self.waypoint_list[t_idx] + t2 * (self.waypoint_list[(t_idx+1)%N] - self.waypoint_list[t_idx])
                dist2 = np.sqrt((pos2d[0]-pt[0])**2 + (pos2d[1]-pt[1])**2) * side
                d2 *= min(1.,max(0.,t2))
            if abs(dist1) < abs(dist2):
                final_dist = dist1
            else :
                final_dist = dist2
            t_closed_refined = t_closed + d1 + d2
            # print("refine time: ", ts-time.time())
            target_pos_list = []
            _, speed, info = self.fn(t_closed_refined, self.path)
            speed *= np.sqrt(mu_factor)
            kin_pos, _, info = self.fn(t_closed_refined+1.2*speed, self.path)
            for i in range(self.H+1):
                # print(speed)
                t = t_closed_refined + i * dt * body_speed
                t_1 = t + dt * speed
                pos, speed, info = self.fn(t, self.path)
                speed *= np.sqrt(mu_factor)
                pos_next, _, info = self.fn(t_1, self.path)
                vel = (pos_next - pos) / dt
                speed_ref = jnp.clip(jnp.linalg.norm(vel), .5, 100.)
                # speed_ref = jnp.clip(jnp.linalg.norm(vel), .5, 100.)
                psi = jnp.arctan2(pos_next[1] - pos[1], pos_next[0] - pos[0])
                # print(speed, speed_ref)
                # print(speed, info['curv'])
                target_pos_list.append(jnp.array([pos[0], pos[1], psi, info['curv'], speed]))
            # print("end time: ", time.time()-ts)
            return jnp.array(target_pos_list), kin_pos, t_closed_refined, final_dist
        
        
    