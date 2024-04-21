import math
import random
import asyncio 
import Sensors
from collections import Counter


def calculate_distance(point_a, point_b):
    '''
    Description: Calculate the distance between two points in 3D space
    Input: point_a, point_b: dictionaries with the keys 'x', 'y', 'z' and the coordinates of the points
    Output: distance: float, distance between the two points
    '''
    distance = math.sqrt((point_b['x'] - point_a['x']) ** 2 +
                         (point_b['y'] - point_a['y']) ** 2 +
                         (point_b['z'] - point_a['z']) ** 2)
    return distance



class DoNothing:
    """
    Description: Class that represents the action of doing nothing
    """
    def __init__(self, a_agent):
        '''
        init method for DoNothing class
        Input: a_agent: Agent object, the agent that will execute the action (in this case, do nothing)
        '''
        # get the agent object
        self.a_agent = a_agent
        # get the agent's sensors
        self.rc_sensor = a_agent.rc_sensor
        # get the agent's internal state
        self.i_state = a_agent.i_state

    async def run(self):
        '''
        Use asyncio to run the action of doing nothing
        Output: True, when the action is done, in this case, after 1 second of sleep
        '''
        #print message to terminal
        print("Doing nothing")
        # sleep for 1 second
        await asyncio.sleep(1)
        # return True when the action is done
        return True



class ForwardDist:
    """
        Moves forward a certain distance specified in the parameter "dist".
        If "dist" is -1, selects a random distance between the initial
        parameters of the class "d_min" and "d_max"
    """
    # Class constants
    STOPPED = 0 # Initial state
    MOVING = 1 # Moving state

    def __init__(self, a_agent, dist, d_min, d_max):
        '''
        init method for ForwardDist class
        Input: a_agent: Agent object, the agent that will execute the action (in this case, move forward)
               dist: float, the distance the agent will move forward
               d_min: float, the minimum distance the agent can move forward
               d_max: float, the maximum distance the agent can move forward
        '''
        # get the agent object
        self.a_agent = a_agent
        # get the agent's sensors
        self.rc_sensor = a_agent.rc_sensor
        # get the agent's internal state
        self.i_state = a_agent.i_state
        # set the original distance
        self.original_dist = dist
        # set the target distance
        self.target_dist = dist
        # set the minimum distance
        self.d_min = d_min
        # set the maximum distance
        self.d_max = d_max
        # set the starting position
        self.starting_pos = a_agent.i_state.position
        # set the state of the agent to STOPPED
        self.state = self.STOPPED

    async def run(self):
        '''
        Use asyncio to run the action of moving forward a certain distance
        Output: True, when the action is done, in this case, after the agent has moved the specified distance
        '''
        # try to run the action
        try:
            while True:
                # if the agent is in the STOPPED state
                if self.state == self.STOPPED:
                    # set starting position before moving
                    self.starting_pos = self.a_agent.i_state.position
                    # Before start moving, calculate the distance we want to move
                    if self.original_dist < 0:
                        # If the distance is negative, select a random distance between d_min and d_max
                        self.target_dist = random.randint(self.d_min, self.d_max)
                    else:
                        # If the distance is positive, set the target distance to the original distance
                        self.target_dist = self.original_dist
                    # Start moving by sending the message "mf" to the agent (move forward)
                    await self.a_agent.send_message("action", "mf")
                    # Set the state to MOVING
                    self.state = self.MOVING
                # if the agent is in the MOVING state
                elif self.state == self.MOVING:
                    #check if we already have covered the required distance
                    current_dist = calculate_distance(self.starting_pos, self.i_state.position)
                    if current_dist >= self.target_dist:
                        # If we have covered the required distance, stop moving
                        await self.a_agent.send_message("action", "stop")
                        # Set the state to STOPPED
                        self.state = self.STOPPED
                        # Return True when the action is done
                        return True
                    # If we haven't covered the required distance
                    else:
                        # sleep 0 secs and Keep moving
                        await asyncio.sleep(0)
                #If the agent is not in the STOPPED or MOVING state
                else:
                    # Print an error message
                    print("Unknown state: " + str(self.state))
                    # Return False
                    return False
        # If the action is cancelled
        except asyncio.CancelledError:
            # Print a message to the terminal
            print("***** TASK Forward CANCELLED")
            # Send the message "stop" to the agent
            await self.a_agent.send_message("action", "stop")
            # Set the state to STOPPED
            self.state = self.STOPPED



class Turn:
    """
    Description: Class that represents the action of turning a certain angle.
    """
    # Class constants
    
    LEFT = -1 # Turn left
    RIGHT = 1 # Turn right
    SELECTING = 0 # Selecting the direction to turn
    TURNING = 1 # Turning

    def __init__(self, a_agent):
        '''
        init method for Turn class
        Input: a_agent: Agent object, the agent that will execute the action (in this case, turn)
        '''
        # get the agent object
        self.a_agent = a_agent
        # get the agent's sensors
        self.rc_sensor = a_agent.rc_sensor
        # get the agent's internal state
        self.i_state = a_agent.i_state
        # set the rotation amount (by default 45 degrees)
        self.rotation_amount = 45
        # set the previous rotation
        self.prev_rotation = 0
        # set the accumulated rotation
        self.accumulated_rotation = 0
        # set the direction to turn (by default right)
        self.direction = self.RIGHT
        # set the state of the agent to SELECTING
        self.state = self.SELECTING

    async def run(self):
        '''
        Use asyncio to run the action of turning a certain angle
        Output: True, when the action is done, in this case, after the agent has turned the specified angle
        '''
        # try to run the action
        try:
            while True:
                # if the agent is in the SELECTING state
                if self.state == self.SELECTING:
                    # Select a random angle between 10 and 90 degrees
                    self.rotation_amount = random.randint(10, 90)
                    #print the angle to the terminal
                    print("Degrees: " + str(self.rotation_amount))
                    # Select a random direction to turn (left or right)
                    self.direction = random.choice([self.LEFT, self.RIGHT])
                    #if the direction is right
                    if self.direction == self.RIGHT:
                        # Send the message "tr" to the agent (turn right)
                        await self.a_agent.send_message("action", "tr")
                    #if the direction is left
                    else:
                        #Send the message "tl" to the agent (turn left)
                        await self.a_agent.send_message("action", "tl")
                    # Set the previous rotation to the current rotation of the agent in the y-axis
                    self.prev_rotation = self.i_state.rotation["y"]
                    # Set the accumulated rotation to 0
                    self.accumulated_rotation = 0
                    # Set the state to TURNING
                    self.state = self.TURNING
                # if the agent is in the TURNING state
                elif self.state == self.TURNING:
                    # Get the current rotation of the agent in the y-axis
                    current_rotation = self.i_state.rotation["y"]
                    # If the direction is right
                    if self.direction == self.RIGHT:
                        #if the previous rotation is greater than the current rotation
                        if self.prev_rotation > current_rotation: 
                            #update the accumulated rotation to the difference between the previous and current rotation (clockwise)
                            self.accumulated_rotation += 360 - self.prev_rotation + current_rotation
                        #if the previous rotation is less than the current rotation
                        else:
                            #update the accumulated rotation to the difference between the current and previous rotation (clockwise)
                            self.accumulated_rotation += current_rotation - self.prev_rotation
                    # If the direction is left
                    else:
                        #if the previous rotation is less than the current rotation
                        if self.prev_rotation < current_rotation: 
                            #update the accumulated rotation to the difference between the current and previous rotation (counter-clockwise)
                            self.accumulated_rotation += 360 - current_rotation + self.prev_rotation
                        #if the previous rotation is greater than the current rotation
                        else:
                            #update the accumulated rotation to the difference between the previous and current rotation (counter-clockwise)
                            self.accumulated_rotation += self.prev_rotation - current_rotation
                    # Set the previous rotation to the current rotation
                    self.prev_rotation = current_rotation
                    # If the accumulated rotation is greater than or equal to the rotation amount
                    if self.accumulated_rotation >= self.rotation_amount:
                        # Send the message "nt" to the agent (no turn)
                        await self.a_agent.send_message("action", "nt")
                        # Reset the accumulated rotation to 0
                        self.accumulated_rotation = 0
                        # Set the direction to right
                        self.direction = self.RIGHT
                        # Set the state to SELECTING
                        self.state = self.SELECTING
                        # Return True when the action is done
                        return True
                # Sleep for 0 seconds and keep running the action
                await asyncio.sleep(0)
        # If the action is cancelled
        except asyncio.CancelledError:
            # Print a message to the terminal
            print("***** TASK Turn CANCELLED")
            # Send the message "nt" to the agent (no turn)
            await self.a_agent.send_message("action", "nt")



class Avoid:
    '''
    Description: Class that represents the action of avoiding obstacles
    '''
    # Class constants
    
    MOVING  = 1 # Moving state
    TURNING = 2 # Turning state

    LEFT = -1 # Turn left
    RIGHT = 1 # Turn right


    def __init__(self, a_agent, rotation_amount):
        '''
        init method for Avoid class
        Input: a_agent: Agent object, the agent that will execute the action (in this case, avoid obstacles)
        '''
        # get the agent object
        self.a_agent = a_agent
        # get the agent's sensors
        self.rc_sensor = a_agent.rc_sensor
        # get the agent's internal state
        self.i_state = a_agent.i_state
        # set the rotation amount (by default 30 degrees)
        #self.rotation_amount = 30
        self.rotation_amount = rotation_amount
        # set the previous rotation
        self.prev_rotation = 0
        # set the accumulated rotation
        self.accumulated_rotation = 0
        # set the direction to turn (by default right)
        self.direction = self.RIGHT
        # set the state of the agent to MOVING
        self.state = self.MOVING
    
    async def run(self):
        '''
        Use asyncio to run the action of avoiding obstacles
        Output: True, when the action is done, in this case, after the agent has avoided the obstacle
        '''
        # try to run the action
        try:
            while True:
                # if the agent is in the MOVING state    
                if self.state == self.MOVING:
                    # Check if any of the rays on the left side of the agent hit any obstacle
                    if any(self.rc_sensor.sensor_rays[Sensors.RayCastSensor.HIT][:5]):
                        # If any of the rays hit, turn right, avoiding the obstacle
                        self.direction == self.RIGHT
                        # Send the message "tr" to the agent (turn right)
                        await self.a_agent.send_message("action", "tr")
                    # Check if any of the rays on the right side of the agent hit any obstacle
                    elif any(self.rc_sensor.sensor_rays[Sensors.RayCastSensor.HIT][5:]):
                        # If any of the rays hit, turn left, avoiding the obstacle
                        self.direction == self.LEFT
                        # Send the message "tl" to the agent (turn left)
                        await self.a_agent.send_message("action", "tl")
                    # Set the previous rotation to the current rotation of the agent in the y-axis
                    self.prev_rotation = self.i_state.rotation["y"]
                    # Set the accumulated rotation to 0
                    self.accumulated_rotation = 0
                    # Set the state to TURNING
                    self.state = self.TURNING

                # if the agent is in the TURNING state
                elif self.state == self.TURNING:
                    # Get the current rotation of the agent in the y-axis
                    current_rotation = self.i_state.rotation["y"]
                    # If the direction is right
                    if self.direction == self.RIGHT:
                        # If the previous rotation is greater than the current rotation
                        if self.prev_rotation > current_rotation: 
                            # Update the accumulated rotation to the difference between the previous and current rotation (clockwise)
                            self.accumulated_rotation += 360 - self.prev_rotation + current_rotation
                        # If the previous rotation is less than the current rotation
                        else:
                            # Update the accumulated rotation to the difference between the current and previous rotation (clockwise)
                            self.accumulated_rotation += current_rotation - self.prev_rotation
                    # If the direction is left
                    else:
                        # If the previous rotation is less than the current rotation
                        if self.prev_rotation < current_rotation: 
                            # Update the accumulated rotation to the difference between the current and previous rotation (counter-clockwise)
                            self.accumulated_rotation += 360 - current_rotation + self.prev_rotation
                        # If the previous rotation is greater than the current rotation
                        else:
                            # Update the accumulated rotation to the difference between the previous and current rotation (counter-clockwise)
                            self.accumulated_rotation += self.prev_rotation - current_rotation
                    # Set the previous rotation to the current rotation
                    self.prev_rotation = current_rotation
                    # Check if the accumulated rotation is greater than or equal to the rotation amount, means that the turn is done:
                    if self.accumulated_rotation >= self.rotation_amount:
                        # Send the message "nt" to the agent (no turn)
                        await self.a_agent.send_message("action", "nt")
                        # Reset the accumulated rotation to 0
                        self.accumulated_rotation = 0
                        # Set the direction to right (default)
                        self.direction = self.RIGHT
                        # Set the state to MOVING
                        self.state = self.MOVING
                        # Return True when the action is done
                        return True
                # Sleep for 0 seconds and keep running the action if the agent has not finish avoiding the obstacle
                await asyncio.sleep(0.1)
        # If the action is cancelled
        except asyncio.CancelledError:
            # Print a message to the terminal
            print("***** TASK Avoid CANCELLED")
            # Send the message "nt" to the agent (no turn)
            await self.a_agent.send_message("action", "nt")
        

class EatFlower:
    '''
    Description: Class that represents the action of eating a flower, to eat in this case
                 is just stopping the agent for 5 seconds next to the flower'''
    def __init__(self, a_agent):
        '''
        init method for EatFlower class
        Input: a_agent: Agent object, the agent that will execute the action (in this case, eat)'''
        # get the agent object
        self.a_agent = a_agent

    async def run(self):
        '''
        Use asyncio to run the action of eating a flower
        Output: True, when the action is done, in this case, after the agent has eaten the flower
        '''
        # Check if the agent is hungry
        if self.a_agent.hungry:
            # Send the message "action" to the agent (stop)
            await self.a_agent.send_message("action", "stop")
            # Sleep for 5 seconds next to the flower
            await asyncio.sleep(5)  
            # Set the agent as not hungry
            self.a_agent.hungry = False
            # Return True when the action is done, the agent has eaten the flower
            return True
        # If the agent is not hungry
        else:
            # Return False, as the agent is not hungry and has not eaten the flower
            return False



class FollowAstronaut:
    '''
    Description: Class that represents the action of following an astronaut
    '''

    # Class constants
    MOVING = 0 # Moving state
    TURNING = 1 # Turning state
    RIGHT = 1 # Turn right
    LEFT = -1 # Turn left

    def __init__(self, a_agent):
        '''
        init method for FollowAstronaut class
        Input: a_agent: Agent object, the agent that will execute the action (in this case, follow an astronaut)
        '''
        # get the agent object
        self.a_agent = a_agent
        # get the agent's sensors
        self.rc_sensor = a_agent.rc_sensor
        # get the agent's internal state
        self.i_state = a_agent.i_state
        # set the rotation amount (by default None)
        self.rotation_amount = None
        # set the previous rotation
        self.prev_rotation = 0
        # set the accumulated rotation
        self.accumulated_rotation = 0
        # set the direction to turn (by default right)
        self.direction = self.RIGHT
        # set the state of the agent to MOVING
        self.state = self.MOVING
        # set the agent as not hungry (by default)
        self.ishungry = False
        
    async def run(self):
        '''
        Use asyncio to run the action of following an astronaut
        Output: True, when the action is done, in this case, after the agent has followed the astronaut
        '''
        # try to run the action
        try:
            # while the agent is not hungry
            while not self.ishungry:
                # if the agent is in the MOVING state
                if self.state == self.MOVING:
                    # Check if any of the rays hits an astronaut, using the detection sensor that we get from the BTCritter.py's detect_astronaut class
                    if self.rc_sensor.sensor_rays[Sensors.RayCastSensor.HIT][self.a_agent.det_sensor]:
                        # if the sensor that detects the astronaut is on the left side of the agent (0-4)
                        if self.a_agent.det_sensor < 5:
                            # Turn left by the angle given by the sensor that detects the astronaut,
                            # if the sensor is 0, turn left by -90 degrees, if it is 4, turn left by -18 degrees
                            turn_angle = -90 + self.a_agent.det_sensor * (90 / 5)
                            # Send the message "tl" to the agent (turn left)
                            await self.a_agent.send_message("action", f"tl")
                        # if the sensor that detects the astronaut is on the right side of the agent (6-10)
                        elif  self.a_agent.det_sensor >5:
                            # Turn right by the angle given by the sensor that detects the astronaut,
                            # if the sensor is 6, turn right by 18 degrees, if it is 10, turn right by 90 degrees
                            turn_angle = self.a_agent.det_sensor * (90 / 5)
                            # Send the message "tr" to the agent (turn right)
                            await self.a_agent.send_message("action", f"tr")
                        # if the sensor that detects the astronaut is in the middle of the agent (5), just move forward, no need to turn
                        else:
                            #set the turn angle to 0 because, if not, we'd get an error of referencing before assignment
                            turn_angle = 0
                            # Send the message "mf" to the agent (move forward)
                            await self.a_agent.send_message("action", f"mf")
                        #set a sleep time to wait for the agent to turn  or move forward
                        await asyncio.sleep(0.15)
                        #go forward another time (this was added empirically to make the agent follow the astronaut better)
                        await self.a_agent.send_message("action", "mf")


                    # If the agent is not in front of an astronaut, but is inside this action, means that the agent recently saw the astronaut
                    #so we go in the direction that we followed the astronaut last time, this is part of the bonus task.
                    else:
                        # Send the message "mf" to the agent (move forward) a couple of times
                        await self.a_agent.send_message("action", "mf")
                        await self.a_agent.send_message("action", "mf")

                    #set previous rotation of the agent to the current rotation 
                    self.prev_rotation = self.i_state.rotation["y"]
                    #set the accumulated rotation to 0
                    self.accumulated_rotation = 0
                    #set the state to TURNING
                    self.state = self.TURNING
                # if the agent is in the TURNING state
                elif self.state == self.TURNING:
                    # Get the current rotation of the agent in the y-axis
                    current_rotation = self.i_state.rotation["y"]
                    # If the direction is right
                    if self.direction == self.RIGHT:
                        # Calculate the rotation change by subtracting the previous rotation from the current rotation and adding 360 to avoid
                        # negative values, then take the modulo 360 so we get the correct value and never does more than an entire rotation (360 degrees)
                        rotation_change = (current_rotation - self.prev_rotation + 360) % 360
                        # Update the accumulated rotation by adding the rotation change
                        self.accumulated_rotation += rotation_change
                    # If the direction is left
                    elif self.direction == self.LEFT:
                        # Calculate the rotation change by subtracting the current rotation from the previous rotation and adding 360 to avoid
                        # negative values, then take the modulo 360 so we get the correct value and never does more than an entire rotation (360 degrees)
                        rotation_change = (self.prev_rotation - current_rotation + 360) % 360
                        # Update the accumulated rotation by adding the rotation change
                        self.accumulated_rotation += rotation_change
                    # Set the previous rotation to the current rotation
                    self.prev_rotation = current_rotation
                    # If the accumulated rotation is greater than or equal to the rotation amount
                    if self.accumulated_rotation >= abs(turn_angle):
                        # Send the message "nt" to the agent (no turn) as the turn is done
                        await self.a_agent.send_message("action", "nt")
                        # Reset the accumulated rotation to 0
                        self.accumulated_rotation = 0
                        # Set the direction to right (default)
                        self.direction = self.RIGHT
                        # Set the state to MOVING
                        self.state = self.MOVING
                        # Return True when the action is done
                        return True
                    # Sleep for 0 seconds and keep running the action
                    await asyncio.sleep(0)
                # If the agent is not in the MOVING or TURNING state
                if not self.a_agent.hungry:
                    # Print an error message
                    self.ishungry = True
        # If the action is cancelled
        except asyncio.CancelledError:
            # Print a message to the terminal
            print("***** TASK Follow CANCELLED")
            # Send the message "nt" to the agent (no turn)
            await self.a_agent.send_message("action", "nt")


