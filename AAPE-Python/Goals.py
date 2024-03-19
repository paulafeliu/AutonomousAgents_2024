import random
import asyncio
import Sensors
from collections import Counter

class Goal:
    """
    Base class for all actions
    """
    a_agent = None

    def __init__(self, a_agent):
        self.a_agent = a_agent
        self.rc_sensor = a_agent.rc_sensor
        self.i_state = a_agent.i_state

        self.prev_currentActions = []
        self.requested_actions = []

    def requested(self, action):
        """
        Checks if the action is already requested
        :return: number of pending request for that action
        """
        return self.requested_actions.count(action)

    def executing(self, action):
        """
        Checks if the action is already executing
        :return: bool
        """
        if action in self.i_state.currentActions:
            return True
        else:
            return False

    def update_req_actions(self):
        """
        Takes the list i_state.currentActions and finds which actions have been added
        with respect prev_currentActions. Then updates the requested_actions list
        accordingly
        :return:
        """
        counter_prev = Counter(self.prev_currentActions)
        counter = Counter(self.i_state.currentActions)

        # New actions executing that were not executing before
        new_actions_executing = list((counter - counter_prev).elements())
        counter_new_actions = Counter(new_actions_executing)
        counter_req_actions = Counter(self.requested_actions)

        # Remove the new actions from the requested_actions list
        # Remove elements in counter_req_actions that are also in counter_new_actions
        for element, count in counter_new_actions.items():
            counter_req_actions[element] -= min(count, counter_req_actions[element])
        # Reconstruct the modified list counter_req_actions
        modified_req_actions = []
        for element, count in counter_req_actions.items():
            modified_req_actions.extend([element] * count)

        self.requested_actions = modified_req_actions

    async def update(self):
        # update requested actions
        self.update_req_actions()
        self.prev_currentActions = self.i_state.currentActions


class DoNothing(Goal):
    """
    Does nothing
    """
    def __init__(self, a_agent):
        super().__init__(a_agent)

    async def update(self):
        await super().update()
        print("Doing nothing")
        await asyncio.sleep(1)

class ForwardStop(Goal):
    """
    Moves forward till it detects an obstacle and then stops
    """
    STOPPED = 0
    MOVING = 1
    END = 2

    state = STOPPED

    def __init__(self, a_agent):
        super().__init__(a_agent)

    async def update(self):
        await super().update()
        if self.state == self.STOPPED:
            # If we are not moving, start moving
            self.requested_actions.append("W")
            await self.a_agent.send_message("action", "W")
            self.state = self.MOVING
            print("MOVING")
        elif self.state == self.MOVING:
            # If we are moving, check if we detect a wall
            sensor_hit = self.rc_sensor.sensor_rays[Sensors.RayCastSensor.HIT]
            if any(ray_hit == 1 for ray_hit in self.rc_sensor.sensor_rays[Sensors.RayCastSensor.HIT]):
                self.requested_actions.append("S")
                await self.a_agent.send_message("action", "S")
                self.state = self.END
                print("END")
            else:
                await asyncio.sleep(0)
        elif self.state == self.END:
            # If we have finished, don't do anything else
            await asyncio.sleep(10)
            print("WAITING")
        else:
            print("Unknown state: " + str(self.state))


class Turn(Goal):
    """
    Repeats the action of turning a random number of degrees in a random
    direction (right or left) A is left, D is right
    """
    
    def __init__(self, a_agent):
        super().__init__(a_agent)
        
    async def update(self):
        await super().update()
        # Choose a random direction to turn
        turn_direction = random.choice(["A", "D"])
        # Choose a random number of degrees to turn
        turn_degrees = random.randint(-100, 100)
        
        turns_needed = abs(turn_degrees//5) # 5 degrees per turn
        
        print(f"Turning {turn_degrees} degrees to the {turn_direction}, in {abs(turns_needed)} turnsteps.")
        async for _ in self.async_turns(turns_needed):
            self.requested_actions.append(turn_direction)
            await self.a_agent.send_message("action", turn_direction)
            await asyncio.sleep(0.5)
        await asyncio.sleep(10)
        
    async def async_turns(self, n):
        for i in range(n):
            yield i
        print("Done turning")

class RandomRoam(Goal):
    """
    Moves around following a direction for a while, changes direction,
    decides to stop, moves again, etc.
    All of this following certain probabilities and maintaining the action during
    a pre-defined amount of time.
    """
    STOPPED = 0
    MOVING = 1
    TURNING = 2
    STOP = 3

    turn_direction = None
    state = STOPPED
    turns = 0
    num_turns = None

    def __init__(self, a_agent):
        super().__init__(a_agent)

    async def next_state(self):
        choice = random.choice([self.TURNING, self.STOP, self.MOVING])
        return choice

    async def update(self):
        await super().update()
       
        if self.state == self.STOPPED:
            # If we are not moving, start moving
            next_state = random.choice([self.TURNING, self.STOP, self.MOVING])
            self.state = next_state
            await asyncio.sleep(1)
            print("Choice: ", next_state)

        #if its choice is moving, start moving and check if there is any obstacle
        elif self.state == self.MOVING:
            self.requested_actions.append("W")
            await self.a_agent.send_message("action", "W")
            print("MOVING")

            if any(ray_hit == 1 for ray_hit in self.rc_sensor.sensor_rays[Sensors.RayCastSensor.HIT]):
                self.requested_actions.append("S")
                await self.a_agent.send_message("action", "S")
                self.state = self.TURNING
                await asyncio.sleep(2)
            else:
                #choose between stopping, forward, turn
                next_state = random.choice([self.TURNING, self.STOP, self.MOVING])
                self.state = next_state
                await asyncio.sleep(2)
                print("Choice: ", next_state)
            await asyncio.sleep(0.1)

        elif self.state == self.STOP:
            self.requested_actions.append("S")
            await self.a_agent.send_message("action", "S")
            await asyncio.sleep(2)

            next_state = random.choice([self.TURNING, self.STOP, self.MOVING])
            self.state = next_state
            await asyncio.sleep(2)
            print("Choice: ", next_state)
           
        elif self.state == self.TURNING:
            if self.turn_direction is None or self.num_turns is None:
                self.requested_actions.append("S")  
                await self.a_agent.send_message("action", "S")
                await asyncio.sleep(1)
                self.turn_direction = random.choice(["A", "D"])  
                self.num_turns = random.randint(1, 70) 
                self.turns = 0  
                print("Direction chosen:", self.turn_direction)
                print("Number of turns:", self.num_turns)
            if self.turns < self.num_turns:
                self.requested_actions.append(self.turn_direction)
                await self.a_agent.send_message("action", self.turn_direction)
                self.turns += 1
                await asyncio.sleep(0.1)  
            else:
                self.turn_direction = None  
                self.num_turns = None  
                next_state = random.choice([self.TURNING, self.STOP, self.MOVING])
                self.state = next_state
                print("Choice: ", next_state)
                await asyncio.sleep(1)
            await asyncio.sleep(0.1)
        else:
            print("Unknown state: " + str(self.state))
    



class Avoid(Goal):
    """
    Moves always forward avoiding obstacles
    """
    STOPPED = 0
    MOVING = 1
    TURNING = 2

    state = STOPPED
    turn_direction = None
    avoid_distance = 0
 
    def __init__(self, a_agent):
        super().__init__(a_agent)

    async def update(self):
        await super().update()
        if self.state == self.STOPPED:
            self.state = self.MOVING
            print("MOVING")

        #if it is moving, check if there is any obstacle
        elif self.state == self.MOVING:
            self.requested_actions.append("W")
            await self.a_agent.send_message("action", "W")

            if any(ray_hit == 1 for ray_hit in self.rc_sensor.sensor_rays[Sensors.RayCastSensor.HIT]):
                self.requested_actions.append("S")
                await self.a_agent.send_message("action", "S")
                print("STOPPING")
                
                #decide the direction of the turn
                if self.rc_sensor.sensor_rays[Sensors.RayCastSensor.HIT][0] == 1:
                    self.turn_direction = "D"
                elif self.rc_sensor.sensor_rays[Sensors.RayCastSensor.HIT][2] == 1:
                    self.turn_direction = "A"
                else:
                    # Choose randomly between left ("A") and right ("D") if the center sensor detects something
                    self.turn_direction = random.choice(["A", "D"])
                
                self.state = self.TURNING
                self.avoid_distance = 0 
                print(f"TURNING: {self.turn_direction}")
            await asyncio.sleep(0.1)
        
        elif self.state == self.TURNING:
            # Turn a little bit to avoid the obstacle
            self.requested_actions.append(self.turn_direction)
            await self.a_agent.send_message("action", self.turn_direction)
            await asyncio.sleep(0.1)
            # Turn a bit to pass the obstacle
            if self.avoid_distance < 3:  
                self.avoid_distance += 1
                await asyncio.sleep(0.1)
            else:
                self.avoid_distance = 0  
                self.state = self.MOVING  
                await  asyncio.sleep(1) 
                print("MOVING FORWARD")
        else:
            print("Unknown state: " + str(self.state))

