import math
import random
import asyncio 
import Sensors
from collections import Counter


def calculate_distance(point_a, point_b):
    distance = math.sqrt((point_b['x'] - point_a['x']) ** 2 +
                         (point_b['y'] - point_a['y']) ** 2 +
                         (point_b['z'] - point_a['z']) ** 2)
    return distance


class DoNothing:
    """
    Does nothing
    """
    def __init__(self, a_agent):
        self.a_agent = a_agent
        self.rc_sensor = a_agent.rc_sensor
        self.i_state = a_agent.i_state

    async def run(self):
        print("Doing nothing")
        await asyncio.sleep(1)
        return True


class ForwardDist:
    """
        Moves forward a certain distance specified in the parameter "dist".
        If "dist" is -1, selects a random distance between the initial
        parameters of the class "d_min" and "d_max"
    """
    STOPPED = 0
    MOVING = 1
    END = 2

    def __init__(self, a_agent, dist, d_min, d_max):
        self.a_agent = a_agent
        self.rc_sensor = a_agent.rc_sensor
        self.i_state = a_agent.i_state
        self.original_dist = dist
        self.target_dist = dist
        self.d_min = d_min
        self.d_max = d_max
        self.starting_pos = a_agent.i_state.position
        self.state = self.STOPPED

    async def run(self):
        try:
            while True:
                if self.state == self.STOPPED:
                    # starting position before moving
                    self.starting_pos = self.a_agent.i_state.position
                    # Before start moving, calculate the distance we want to move
                    if self.original_dist < 0:
                        self.target_dist = random.randint(self.d_min, self.d_max)
                    else:
                        self.target_dist = self.original_dist
                    # Start moving
                    await self.a_agent.send_message("action", "mf")
                    self.state = self.MOVING
                    # print("TARGET DISTANCE: " + str(self.target_dist))
                    # print("MOVING ")
                elif self.state == self.MOVING:
                    # If we are moving, check if we already have covered the required distance
                    current_dist = calculate_distance(self.starting_pos, self.i_state.position)
                    if current_dist >= self.target_dist:
                        await self.a_agent.send_message("action", "stop")
                        self.state = self.STOPPED
                        return True
                    else:
                        await asyncio.sleep(0)
                else:
                    print("Unknown state: " + str(self.state))
                    return False
        except asyncio.CancelledError:
            print("***** TASK Forward CANCELLED")
            await self.a_agent.send_message("action", "stop")
            self.state = self.STOPPED


class Turn:
    """
    Repeats the action of turning a random number of degrees in a random
    direction (right or left)
    """
    LEFT = -1
    RIGHT = 1

    SELECTING = 0
    TURNING = 1

    def __init__(self, a_agent):
        self.a_agent = a_agent
        self.rc_sensor = a_agent.rc_sensor
        self.i_state = a_agent.i_state
        self.rotation_amount = 45
        self.prev_rotation = 0
        self.accumulated_rotation = 0
        self.direction = self.RIGHT
        self.state = self.SELECTING

    async def run(self):
        try:
            while True:
                if self.state == self.SELECTING:
                    self.rotation_amount = random.randint(10, 90)
                    print("Degrees: " + str(self.rotation_amount))
                    self.direction = random.choice([self.LEFT, self.RIGHT])
                    if self.direction == self.RIGHT:
                        await self.a_agent.send_message("action", "tr")
                        # print("Direction: RIGHT")
                    else:
                        await self.a_agent.send_message("action", "tl")
                        # print("Direction: LEFT")
                    self.prev_rotation = self.i_state.rotation["y"]
                    self.accumulated_rotation = 0
                    self.state = self.TURNING
                    # print("TURNING...")
                elif self.state == self.TURNING:
                    # check if we have finished the rotation
                    current_rotation = self.i_state.rotation["y"]
                    if self.direction == self.RIGHT:
                        if self.prev_rotation > current_rotation: # complete 360 turn clockwise
                            self.accumulated_rotation += 360 - self.prev_rotation + current_rotation
                        else:
                            self.accumulated_rotation += current_rotation - self.prev_rotation
                    else:
                        if self.prev_rotation < current_rotation: # complete 260 turn counter-clockwise
                            self.accumulated_rotation += 360 - current_rotation + self.prev_rotation
                        else:
                            self.accumulated_rotation += self.prev_rotation - current_rotation
                    self.prev_rotation = current_rotation

                    if self.accumulated_rotation >= self.rotation_amount:
                        # We are there
                        # print("TURNING DONE.")
                        await self.a_agent.send_message("action", "nt")
                        self.accumulated_rotation = 0
                        self.direction = self.RIGHT
                        self.state = self.SELECTING
                        return True
                await asyncio.sleep(0)
        except asyncio.CancelledError:
            print("***** TASK Turn CANCELLED")
            await self.a_agent.send_message("action", "nt")

class Avoid:

    MOVING  = 1
    TURNING = 2

    LEFT = -1
    RIGHT = 1

    #turn_direction = None
    #rotation_amount = 45
    #prev_rotation = 0
    #accumulated_rotation = 0

    def __init__(self, a_agent):
        #self.a_agent = a_agent
        #self.rc_sensor = a_agent.rc_sensor
        self.a_agent = a_agent
        self.rc_sensor = a_agent.rc_sensor
        self.i_state = a_agent.i_state
        self.rotation_amount = 45
        self.prev_rotation = 0
        self.accumulated_rotation = 0
        self.direction = self.RIGHT
        self.state = self.MOVING
        
    
    async def run(self):
        print("inside avoid")
        try:
            while True:
                    
                if self.state == self.MOVING:
                    #if any(ray_hit == 1 for ray_hit in self.rc_sensor.sensor_rays[Sensors.RayCastSensor.HIT]):
                        #sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
                        #obstacle_angle = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.ANGLE]

                    if any(self.rc_sensor.sensor_rays[Sensors.RayCastSensor.HIT][:5]):
                        self.direction == self.RIGHT
                        print("turn right")
                        #self.turn_direction = "tr"
                        await self.a_agent.send_message("action", "tr")

                    elif any(self.rc_sensor.sensor_rays[Sensors.RayCastSensor.HIT][5:]):
                        self.direction == self.LEFT
                        print("turn left")
                        #self.turn_direction = "tl"
                        await self.a_agent.send_message("action", "tl")

                #await self.a_agent.send_message("action", self.turn_direction)

                #print(f"TURNING: {self.turn_direction}")

                    self.prev_rotation = self.i_state.rotation["y"]
                    self.accumulated_rotation = 0
                    self.state = self.TURNING

                elif self.state == self.TURNING:
                    current_rotation = self.i_state.rotation["y"]

                    if self.direction == self.RIGHT:
                        if self.prev_rotation > current_rotation: # complete 360 turn clockwise
                            self.accumulated_rotation += 360 - self.prev_rotation + current_rotation
                        else:
                            self.accumulated_rotation += current_rotation - self.prev_rotation
                    else:
                        if self.prev_rotation < current_rotation: # complete 260 turn counter-clockwise
                            self.accumulated_rotation += 360 - current_rotation + self.prev_rotation
                        else:
                            self.accumulated_rotation += self.prev_rotation - current_rotation
                    self.prev_rotation = current_rotation

                    if self.accumulated_rotation >= self.rotation_amount:
                        # We are there
                        # print("TURNING DONE.")
                        await self.a_agent.send_message("action", "nt")
                        self.accumulated_rotation = 0
                        self.direction = self.RIGHT
                        self.state = self.MOVING
                        return True
            #await asyncio.sleep(0)

                await asyncio.sleep(0)
                
        except asyncio.CancelledError:
            print("***** TASK Turn CANCELLED")
            await self.a_agent.send_message("action", "nt")
        
        #return True

class EatFlower:
    def __init__(self, a_agent, hungry_flag):
        self.a_agent = a_agent
        self.hungry_flag = hungry_flag

    async def run(self):
        print("inside eatflower")

        if self.hungry_flag:
        #and 'Flower' in [obj['tag'] for obj in self.a_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]]:
            #await self.a_agent.send_message("action", "move_to_flower")
            print("feeding")
            await asyncio.sleep(5)  # Stay near the flower
            self.hungry_flag = False
            #asyncio.get_event_loop().call_later(15, self.set_hungry)
            return True
        return False


                


