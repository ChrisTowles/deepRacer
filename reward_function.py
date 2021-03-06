# Place import statement outside of function (supported libraries: math, random, numpy, scipy, and shapely)
# Example imports of available libraries
#
# import random
# import numpy as np
# import scipy
# import shapely
import math


# '''
#    Example of rewarding the agent to follow center line
#
#    "all_wheels_on_track": Boolean,        # flag to indicate if the agent is on the track
#    "x": float,                            # agent's x-coordinate in meters
#    "y": float,                            # agent's y-coordinate in meters
#    "closest_objects": [int, int],         # zero-based indices of the two closest objects to the agent's current position of (x, y).
#    "closest_waypoints": [int, int],       # indices of the two nearest waypoints.
#    "distance_from_center": float,         # distance in meters from the track center
#    "is_crashed": Boolean,                 # Boolean flag to indicate whether the agent has crashed.
#    "is_left_of_center": Boolean,          # Flag to indicate if the agent is on the left side to the track center or not.
#    "is_offtrack": Boolean,                # Boolean flag to indicate whether the agent has gone off track.
#    "is_reversed": Boolean,                # flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
#    "heading": float,                      # agent's yaw in degrees
#    "objects_distance": [float, ],         # list of the objects' distances in meters between 0 and track_length in relation to the starting line.
#    "objects_heading": [float, ],          # list of the objects' headings in degrees between -180 and 180.
#    "objects_left_of_center": [Boolean, ], # list of Boolean flags indicating whether elements' objects are left of the center (True) or not (False).
#    "objects_location": [(float, float),], # list of object locations [(x,y), ...].
#    "objects_speed": [float, ],            # list of the objects' speeds in meters per second.
#    "progress": float,                     # percentage of track completed
#    "speed": float,                        # agent's speed in meters per second (m/s)
#    "steering_angle": float,               # agent's steering angle in degrees
#    "steps": int,                          # number steps completed
#    "track_length": float,                 # track length in meters.
#    "track_width": float,                  # width of the track
#    "waypoints": [(float, float), ]        # list of (x,y) as milestones along the track center
#    '''

def reward_function(params) -> float:
    # Read input parameters
    all_wheels_on_track: bool = params['all_wheels_on_track']
    speed = params['speed']
    current_point = [float(params['x']), float(params['y'])]
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    progress: float = params['progress']

    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    steering_angle = params['steering_angle']

    waypoint_calc_response = calc_reward_from_waypoint_vs_heading(waypoints=waypoints,
                                                                  closest_waypoints=closest_waypoints,
                                                                  heading=heading,
                                                                  steering_angle=steering_angle,
                                                                  current_point=current_point,
                                                                  lookahead_by=1)

    speed_reward = calc_wheels_on_track_and_speed(all_wheels_on_track=all_wheels_on_track, speed=speed, delta_in_heading=waypoint_calc_response.delta_in_heading)
    # steering_reward = calc_abs_steering(steering_angle=steering_angle)
    # center_line_reward = calc_center_line(distance_from_center=distance_from_center, track_width=track_width)

    # should help go faster in straight ways
    final_reward = waypoint_calc_response.reward

    # reward it for doing good
    if progress == 100:
        final_reward += 100

    # helps with unit tests
    if final_reward < 1e-3:
        final_reward = 1e-3

    return round(final_reward, 4)


def calc_wheels_on_track_and_speed(all_wheels_on_track: bool, speed: float, delta_in_heading: float) -> float:
    # Initialize the reward with typical value
    local_reward = 1.0

    # Set the speed threshold based your action space
    SPEED_THRESHOLD = 1.5
    DELTA_IN_HEADING_THRESHOLD = 10
    if not all_wheels_on_track:
        # Penalize if the car goes off track
        local_reward = 1e-3  # off track = bad
    elif DELTA_IN_HEADING_THRESHOLD > delta_in_heading and speed < SPEED_THRESHOLD:
        # Penalize if the car goes too slow
        local_reward *= 0.6

    return local_reward


def calc_abs_steering(steering_angle: float) -> float:
    # Initialize the reward with typical value
    local_reward = 1.0

    abs_steering = abs(steering_angle)

    # Penalize if car steer too much to prevent zigzag
    ABS_STEERING_THRESHOLD = 15.0
    if abs_steering > ABS_STEERING_THRESHOLD:
        local_reward *= 0.8

    return local_reward


class WaypointCalcResult:
    def __init__(self, needed_heading: float, delta_in_steering: float, delta_in_heading: float, reward: float):
        self.needed_heading: float = round(needed_heading, 4)
        self.delta_in_steering: float = round(delta_in_steering, 4)
        self.delta_in_heading: float = round(delta_in_heading, 4)
        self.reward: float = round(reward, 4)


def calc_reward_from_waypoint_vs_heading(waypoints, closest_waypoints, heading: float, steering_angle: float,
                                         current_point,
                                         lookahead_by: int = 3) -> WaypointCalcResult:
    # Initialize the reward with typical value
    local_reward = 1.0
    # Calculate the direction of the center line based on the closest waypoints
    # from https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-reward-function-input.html#reward-function-input-closest_waypoints

    # next_avg_point = get_waypoint_look_ahead_average_point(closest_waypoints, waypoints, lookahead_by=lookahead_by)
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # track_direction = get_angle_between_points(next_point=next_avg_point, prev_point=prev_point)
    track_heading = get_angle_between_points(next_avg_point=next_point, prev_point=prev_point)
    delta_in_heading = track_heading - heading
    # what if already steering, lets see diff from our heading.
    delta_in_steering = abs(steering_angle - delta_in_heading)

    MIN_HEADING_DELTA_ALLOWED_IN_DEGREES = 10
    MAX_HEADING_DELTA_ALLOWED_IN_DEGREES = 40

    if abs(delta_in_heading) > MIN_HEADING_DELTA_ALLOWED_IN_DEGREES:

        # if we are more than 40 % just give up.
        if abs(delta_in_heading) >= MAX_HEADING_DELTA_ALLOWED_IN_DEGREES:
            local_reward = 1e-3
        else:
            # set the reward to get worse as we get away from zero
            # 1-abs(5/40) => 1-0.125 => 8.75
            # 1-abs(20/40) => 1-0.500 => 5.50
            local_reward = 1 - abs(delta_in_heading / MAX_HEADING_DELTA_ALLOWED_IN_DEGREES)

    # made this an object so i can test the steps
    return WaypointCalcResult(needed_heading=track_heading,
                              delta_in_heading=delta_in_heading,
                              delta_in_steering=delta_in_steering,
                              reward=local_reward)


def get_waypoint_look_ahead_average_point(closest_waypoints, waypoints, lookahead_by: int):
    next_few_points = waypoints[closest_waypoints[1]:lookahead_by]

    # took out due to numpy issue
    # next_avg_point = numpy.average(numpy.array(next_few_points), axis=0)

    # take default values if can' get list
    next_avg_point = waypoints[closest_waypoints[1]]
    if len(next_few_points) > 0:
        x_sum = sum(point[0] for point in next_few_points)
        y_sum = sum(point[1] for point in next_few_points)

        avg_x = x_sum / len(next_few_points)
        avg_y = y_sum / len(next_few_points)
        next_avg_point = [avg_x, avg_y]

    return next_avg_point


def get_angle_between_points(prev_point, next_avg_point):
    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_avg_point[1] - prev_point[1], next_avg_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    return track_direction


def calc_center_line(distance_from_center: float, track_width: float) -> float:
    '''
        example 
        https://github.com/aws-samples/aws-deepracer-workshops/blob/master/Advanced%20workshops/reInvent2019-400/customize/reward_advanced.py

    '''
    local_reward = 1e-3

    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        local_reward = 1.0
    elif distance_from_center <= marker_2:
        local_reward = 0.5
    elif distance_from_center <= marker_3:
        local_reward = 0.1

    return local_reward
